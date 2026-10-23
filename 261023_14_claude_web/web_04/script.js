// ===== 공통: 기록 저장 =====
const TAPE_KEY = "calc-tape";
const TAPE_LIMIT = 50;

// 개인 창이나 저장소가 막힌 브라우저에서는 localStorage가 에러를 내므로 감싸서 쓴다
function loadTape() {
  try {
    return JSON.parse(localStorage.getItem(TAPE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveTape() {
  try {
    localStorage.setItem(TAPE_KEY, JSON.stringify(tape));
  } catch {
    // 저장하지 못해도 계산기는 그대로 쓸 수 있다
  }
}

// ===== 상태 =====
let tokens = [];            // 지금까지 확정된 숫자와 연산자. 예: [12, "+", 8, "×"]
let current = "0";          // 지금 입력 중인 숫자 (문자열). 연산자 직후에는 ""
let justEvaluated = false;  // 방금 = 을 눌렀는지
let lastExpr = "";          // = 을 누른 수식 (화면 윗줄에 보여줌)
let tape = loadTape();      // 계산 기록 [{ expr, result }]

const exprEl = document.getElementById("expr");
const resultEl = document.getElementById("result");
const tapeList = document.getElementById("tape-list");
const tapeRoll = document.getElementById("tape-roll");
const tapeEmpty = document.getElementById("tape-empty");
const themeSwitch = document.getElementById("theme-switch");

// ===== 계산 =====
// 0.1 + 0.2 = 0.30000000000000004 같은 소수 오차를 12자리에서 반올림해 정리한다
function tidy(number) {
  return parseFloat(number.toPrecision(12));
}

// [숫자, 연산자, 숫자, 연산자, 숫자 ...] 배열을 계산한다 (eval 을 쓰지 않음)
// 1단계: 왼쪽부터 × ÷ 만 먼저 계산해서 [숫자, +/−, 숫자 ...] 로 줄인다
//        예) [2, "+", 3, "×", 4] → [2, "+", 12]
// 2단계: 남은 + − 를 왼쪽부터 차례로 계산한다
//        예) [2, "+", 12] → 14
function calculate(list) {
  const stack = [list[0]];
  for (let i = 1; i < list.length; i += 2) {
    const op = list[i];
    const num = list[i + 1];
    const last = stack.length - 1;
    if (op === "×") {
      stack[last] = stack[last] * num;
    } else if (op === "÷") {
      stack[last] = num === 0 ? 0 : stack[last] / num;  // 0으로 나누면 0으로 처리
    } else {
      stack.push(op, num);
    }
  }

  let total = stack[0];
  for (let i = 1; i < stack.length; i += 2) {
    total = stack[i] === "+" ? total + stack[i + 1] : total - stack[i + 1];
  }
  return tidy(total);
}

// ===== 입력 처리 =====
// 모든 입력을 지우고 처음 상태로 돌아간다
function clearAll() {
  tokens = [];
  current = "0";
  justEvaluated = false;
  lastExpr = "";
}

// 숫자 키: 입력 중인 숫자 뒤에 붙인다
function inputDigit(digit) {
  if (justEvaluated) clearAll();
  if (current.replace(/[-.]/g, "").length >= 15) return;  // 너무 긴 숫자는 막는다
  if (current === "0") current = digit;
  else if (current === "-0") current = "-" + digit;
  else current += digit;
}

// 소수점 키: 한 숫자에 한 번만 들어간다
function inputDot() {
  if (justEvaluated) clearAll();
  if (current === "") current = "0";
  if (!current.includes(".")) current += ".";
}

// 연산자 키: 입력 중인 숫자를 확정하고 연산자를 붙인다
function inputOperator(op) {
  justEvaluated = false;  // = 직후라면 결과(current)에 이어서 계산한다
  if (current === "") {
    tokens[tokens.length - 1] = op;  // 연산자를 연속으로 누르면 마지막 것으로 바꾼다
    return;
  }
  tokens.push(Number(current), op);
  current = "";
}

// ± 키: 입력 중인 숫자의 부호를 바꾼다
function toggleSign() {
  if (current === "" || Number(current) === 0) return;
  current = current.startsWith("-") ? current.slice(1) : "-" + current;
  justEvaluated = false;
}

// % 키: 입력 중인 숫자를 100으로 나눈다
function percent() {
  if (current === "") return;
  current = String(tidy(Number(current) / 100));
  justEvaluated = false;
}

// Backspace: 한 글자 지운다. 숫자가 비어 있으면 앞의 연산자를 지운다
function backspace() {
  if (justEvaluated) return;
  if (current !== "") {
    current = current.slice(0, -1);
    if (current === "" || current === "-") current = tokens.length === 0 ? "0" : "";
  } else if (tokens.length > 0) {
    tokens.pop();                       // 연산자 제거
    current = String(tokens.pop());     // 그 앞의 숫자를 다시 입력 중으로
  }
}

// = 키: 수식을 계산하고 테이프에 한 줄 찍는다
function equals() {
  if (tokens.length === 0) return;      // 연산자가 없으면 계산할 것이 없다
  const list = current === "" ? tokens.slice(0, -1) : [...tokens, Number(current)];
  const result = calculate(list);

  lastExpr = list.map(formatToken).join(" ");
  printToTape(lastExpr, result);

  tokens = [];
  current = String(result);
  justEvaluated = true;
}

// ===== 화면 표시 =====
// 숫자에 세 자리마다 쉼표를 넣는다. 입력 중인 "12." 같은 문자열도 그대로 유지한다
function withCommas(text) {
  const [intPart, decPart] = text.split(".");
  const sign = intPart.startsWith("-") ? "-" : "";
  const digits = intPart.replace("-", "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return sign + digits + (decPart !== undefined ? "." + decPart : "");
}

function formatToken(token) {
  return typeof token === "number" ? withCommas(String(token)) : token;
}

// 결과가 화면보다 길면 글자 크기를 2px씩 줄인다
function fitResult() {
  let size = 44;
  resultEl.style.fontSize = size + "px";
  while (resultEl.scrollWidth > resultEl.clientWidth && size > 18) {
    size -= 2;
    resultEl.style.fontSize = size + "px";
  }
}

// 현재 상태를 화면 두 줄(수식, 숫자)에 그린다
function render() {
  exprEl.textContent = justEvaluated ? lastExpr + " =" : tokens.map(formatToken).join(" ");
  const shown = current !== "" ? current : String(tokens[tokens.length - 2]);
  resultEl.textContent = withCommas(shown);
  fitResult();
}

// ===== 테이프 (계산 기록) =====
// 새 기록을 추가하고, 50개를 넘으면 오래된 것부터 버린다
function printToTape(expr, result) {
  tape.push({ expr, result });
  if (tape.length > TAPE_LIMIT) tape = tape.slice(-TAPE_LIMIT);
  saveTape();
  renderTape();

  // 한 줄만큼 밀려 올라가는 효과 (클래스를 뗐다 붙여 애니메이션을 다시 실행)
  tapeList.classList.remove("printed");
  void tapeList.offsetWidth;
  tapeList.classList.add("printed");
}

// 테이프 목록을 다시 그리고 최신 줄(맨 아래)로 스크롤한다
function renderTape() {
  tapeList.innerHTML = "";
  tape.forEach((item) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "tape-item";
    button.setAttribute("aria-label", `${item.expr} = ${item.result}, 결과 불러오기`);

    const expr = document.createElement("span");
    expr.className = "tape-expr";
    expr.textContent = item.expr + " =";
    const result = document.createElement("span");
    result.className = "tape-result";
    result.textContent = withCommas(String(item.result));

    button.append(expr, result);
    button.addEventListener("click", () => recallResult(item.result));
    li.append(button);
    tapeList.append(li);
  });

  tapeEmpty.hidden = tape.length > 0;
  tapeRoll.scrollTop = tapeRoll.scrollHeight;
}

// 테이프 항목을 누르면 그 결과 숫자를 불러와 이어서 계산할 수 있게 한다
function recallResult(result) {
  if (justEvaluated) clearAll();
  current = String(result);
  render();
}

function clearTape() {
  tape = [];
  saveTape();
  renderTape();
}

// ===== 테마 (저장하지 않음: 새로 열면 시스템 설정을 따른다) =====
function setTheme(dark) {
  document.documentElement.dataset.theme = dark ? "dark" : "light";
  themeSwitch.setAttribute("aria-checked", String(dark));
}

// ===== 이벤트 연결 =====
// 키패드 버튼 하나를 눌렀을 때 어떤 동작인지 data- 속성으로 구분한다
function handleKey(button) {
  const { digit, op, action } = button.dataset;
  if (digit !== undefined) inputDigit(digit);
  else if (op) inputOperator(op);
  else if (action === "clear") clearAll();
  else if (action === "sign") toggleSign();
  else if (action === "percent") percent();
  else if (action === "dot") inputDot();
  else if (action === "equals") equals();
  render();
}

document.querySelectorAll(".keys .key").forEach((button) => {
  button.addEventListener("click", () => handleKey(button));
});

// 키보드 입력을 계산기 동작으로 바꾼다
const KEY_OPS = { "+": "+", "-": "−", "*": "×", "/": "÷" };

document.addEventListener("keydown", (event) => {
  const key = event.key;
  if (event.ctrlKey || event.metaKey || event.altKey) return;  // Ctrl+C 같은 단축키는 건드리지 않는다

  if (/^[0-9]$/.test(key)) inputDigit(key);
  else if (key === ".") inputDot();
  else if (KEY_OPS[key]) inputOperator(KEY_OPS[key]);
  else if (key === "Enter" || key === "=") equals();
  else if (key === "Backspace") backspace();
  else if (key === "Escape") clearAll();
  else if (key === "%") percent();
  else return;

  event.preventDefault();  // 버튼에 포커스가 있을 때 Enter 가 두 번 눌리는 것을 막는다
  render();
});

document.getElementById("tape-clear").addEventListener("click", clearTape);

themeSwitch.addEventListener("click", () => {
  setTheme(themeSwitch.getAttribute("aria-checked") !== "true");
});

// ===== 시작 =====
setTheme(window.matchMedia("(prefers-color-scheme: dark)").matches);
renderTape();
render();
document.fonts.ready.then(fitResult);  // 도트 글꼴이 늦게 로딩되면 글자 폭이 바뀌므로 크기를 다시 맞춘다
