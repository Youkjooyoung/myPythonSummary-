// ===== 상태 =====
let tokens = [];            // 지금까지 확정된 숫자와 연산자. 예: [12, "+", 8, "×"]
let current = "0";          // 지금 입력 중인 숫자 (문자열). 연산자 직후에는 ""
let justEvaluated = false;  // 방금 = 을 눌렀는지
let lastExpr = "";          // = 을 누른 수식 (화면 윗줄에 보여줌)

const MAX_DIGITS = 15;      // 한 숫자에 입력할 수 있는 최대 자릿수

const exprEl = document.getElementById("expr");
const resultEl = document.getElementById("result");
const toastEl = document.getElementById("toast");
const keyButtons = document.querySelectorAll(".key");

// ===== 숫자 다루기 =====
// 0.1 + 0.2 = 0.30000000000000004 같은 부동소수점 오차를 12자리에서 정리
function clean(x) {
  return parseFloat(x.toPrecision(12));
}

// 계산 결과(숫자)를 입력 문자열로 바꾼다. 아주 크거나 작으면 지수 표기
function numberToString(x) {
  const abs = Math.abs(x);
  if (abs >= 1e16 || (abs !== 0 && abs < 1e-9)) {
    return x.toExponential(8).replace(/\.?0+e/, "e");
  }
  return String(x);
}

// 화면 표시용: 정수 부분에 천 단위 쉼표. 입력 중인 "12." 이나 "0.50" 도 그대로 보여준다
function formatNumber(str) {
  if (str === "" || str.includes("e")) return str;
  const negative = str.startsWith("-");
  const [intPart, decPart] = str.replace("-", "").split(".");
  const intText = Number(intPart || "0").toLocaleString("ko-KR");
  const decText = decPart !== undefined ? "." + decPart : "";
  return (negative ? "-" : "") + intText + decText;
}

function formatTokens(list) {
  return list
    .map((t) => (typeof t === "number" ? formatNumber(numberToString(t)) : t))
    .join(" ");
}

// ===== 계산: × ÷ 먼저, 그다음 + − =====
// 0으로 나누면 null, 너무 커지면 Infinity 를 돌려준다
function evaluate(list) {
  const stack = [list[0]];
  for (let i = 1; i < list.length; i += 2) {
    const op = list[i];
    const n = list[i + 1];
    if (op === "×") {
      stack[stack.length - 1] *= n;
    } else if (op === "÷") {
      if (n === 0) return null;
      stack[stack.length - 1] /= n;
    } else {
      stack.push(op, n);
    }
  }

  let total = stack[0];
  for (let i = 1; i < stack.length; i += 2) {
    total = stack[i] === "+" ? total + stack[i + 1] : total - stack[i + 1];
  }
  return clean(total);
}

// ===== 입력 처리 =====
function inputDigit(d) {
  if (justEvaluated) {
    tokens = [];
    current = "";
    lastExpr = "";
    justEvaluated = false;
  }
  if (current === "0") {
    current = d;
  } else if (current === "-0") {
    current = "-" + d;
  } else if (current.replace(/[-.]/g, "").length < MAX_DIGITS) {
    current += d;
  }
}

function inputDot() {
  if (justEvaluated) {
    tokens = [];
    current = "0";
    lastExpr = "";
    justEvaluated = false;
  }
  if (current === "") current = "0";
  if (current.includes("e")) return;
  if (!current.includes(".")) current += ".";
}

function inputOperator(op) {
  if (justEvaluated) {
    // 결과에 이어서 계산한다
    lastExpr = "";
    justEvaluated = false;
  }
  if (current === "") {
    // 연산자를 연달아 누르면 마지막 것으로 바꾼다
    if (tokens.length > 0) tokens[tokens.length - 1] = op;
    return;
  }
  tokens.push(Number(current), op);
  current = "";
}

function calculate() {
  if (tokens.length === 0) return;

  const list = [...tokens];
  if (current === "") {
    list.pop(); // "12 +" 처럼 연산자로 끝나면 그 연산자는 버린다
  } else {
    list.push(Number(current));
  }

  const result = evaluate(list);
  if (result === null) {
    showToast("0으로는 나눌 수 없어요");
    return;
  }
  if (!Number.isFinite(result)) {
    showToast("숫자가 너무 커서 계산할 수 없어요");
    return;
  }

  lastExpr = formatTokens(list) + " =";
  current = numberToString(result);
  tokens = [];
  justEvaluated = true;
  playResultAnimation();
}

function percent() {
  if (current === "" || current.includes("e")) return;
  current = numberToString(clean(Number(current) / 100));
}

function negate() {
  if (current === "" || Number(current) === 0) return;
  current = current.startsWith("-") ? current.slice(1) : "-" + current;
}

function backspace() {
  if (justEvaluated) {
    // 결과는 남기고 윗줄 수식만 지운다
    lastExpr = "";
    justEvaluated = false;
    return;
  }
  if (current === "") {
    // 방금 누른 연산자를 지우고 앞 숫자를 다시 고칠 수 있게 꺼낸다
    if (tokens.length > 0) {
      tokens.pop();
      current = numberToString(tokens.pop());
    }
    return;
  }
  current = current.includes("e") ? "" : current.slice(0, -1);
  if (current === "" || current === "-") {
    current = tokens.length > 0 ? "" : "0";
  }
}

function clearAll() {
  tokens = [];
  current = "0";
  justEvaluated = false;
  lastExpr = "";
}

function press(key) {
  if (/^[0-9]$/.test(key)) inputDigit(key);
  else if (key === ".") inputDot();
  else if (["+", "−", "×", "÷"].includes(key)) inputOperator(key);
  else if (key === "=") calculate();
  else if (key === "%") percent();
  else if (key === "neg") negate();
  else if (key === "back") backspace();
  else if (key === "clear") clearAll();
  render();
}

// ===== 화면 그리기 =====
function render() {
  exprEl.textContent = justEvaluated ? lastExpr : formatTokens(tokens);

  // 연산자 직후에는 바로 앞 숫자를 크게 보여준다
  const shown = current !== "" ? current : numberToString(tokens[tokens.length - 2]);
  const text = formatNumber(shown);
  resultEl.textContent = text;
  resultEl.classList.toggle("is-long", text.length > 9 && text.length <= 13);
  resultEl.classList.toggle("is-longer", text.length > 13);

  // 눌러 둔 연산자 키를 표시
  const pendingOp = current === "" ? tokens[tokens.length - 1] : null;
  document.querySelectorAll(".key--op").forEach((btn) => {
    const on = btn.dataset.key === pendingOp;
    btn.classList.toggle("is-pending", on);
    btn.setAttribute("aria-pressed", on);
  });
}

function playResultAnimation() {
  resultEl.classList.remove("is-new");
  void resultEl.offsetWidth; // 애니메이션을 처음부터 다시 재생
  resultEl.classList.add("is-new");
}

let toastTimer;
function showToast(message) {
  toastEl.textContent = message;
  toastEl.classList.add("is-visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.remove("is-visible"), 2000);
}

// ===== 이벤트: 마우스·터치 =====
keyButtons.forEach((btn) => {
  btn.addEventListener("click", () => press(btn.dataset.key));
});

// ===== 이벤트: 키보드 =====
const KEYBOARD_MAP = {
  "+": "+",
  "-": "−",
  "*": "×",
  "x": "×",
  "/": "÷",
  "=": "=",
  "Enter": "=",
  "%": "%",
  ".": ".",
  ",": ".",
  "Backspace": "back",
  "Escape": "clear",
  "Delete": "clear",
};

document.addEventListener("keydown", (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const key = /^[0-9]$/.test(e.key) ? e.key : KEYBOARD_MAP[e.key];
  if (!key) return;

  e.preventDefault(); // Enter가 포커스된 버튼까지 눌러 두 번 입력되는 것을 막는다
  press(key);
  flashKey(key);
});

// 키보드로 누른 키도 화면의 버튼이 눌린 것처럼 보이게
function flashKey(key) {
  const btn = document.querySelector(`.key[data-key="${key}"]`);
  if (!btn) return;
  btn.classList.add("is-pressed");
  setTimeout(() => btn.classList.remove("is-pressed"), 120);
}

render();
