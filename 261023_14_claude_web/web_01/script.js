// ===== 계산기 상태 =====
let current = "0";        // 지금 화면에 입력 중인 숫자 (문자열)
let previous = null;      // 연산자 앞의 숫자
let operator = null;      // 선택한 연산자 (+, -, *, /)
let waitingForNext = false; // 연산자를 누른 직후인지 (다음 숫자를 새로 입력해야 함)
let errorMessage = null;  // 에러가 나면 화면에 잠깐 띄울 문구

const MAX_LENGTH = 15;
const SYMBOLS = { "+": "+", "-": "−", "*": "×", "/": "÷" };

const expressionEl = document.getElementById("expression");
const currentEl = document.getElementById("current");

// ===== 계산 =====
function calculate(a, b, op) {
  switch (op) {
    case "+": return a + b;
    case "-": return a - b;
    case "*": return a * b;
    case "/": return b === 0 ? null : a / b; // 0으로 나누기는 null로 표시
  }
}

// 0.1 + 0.2 = 0.30000000000000004 같은 소수 오차를 정리
function tidy(num) {
  return String(parseFloat(num.toPrecision(12)));
}

// ===== 입력 처리 =====
function inputDigit(digit) {
  if (waitingForNext) {
    current = digit;
    waitingForNext = false;
  } else if (current.replace(/[-.]/g, "").length < MAX_LENGTH) {
    current = current === "0" ? digit : current + digit;
  }
}

function inputDot() {
  if (waitingForNext) {
    current = "0.";
    waitingForNext = false;
  } else if (!current.includes(".")) {
    current += ".";
  }
}

function chooseOperator(op) {
  // 연산자를 연달아 누르면 마지막 것으로 바꾸기만 한다
  if (operator && waitingForNext) {
    operator = op;
    return;
  }

  // 이미 연산자가 있으면 지금까지 결과를 먼저 계산 (예: 2 + 3 × → 5 ×)
  if (operator) {
    const result = calculate(previous, parseFloat(current), operator);
    if (result === null) return showError();
    current = tidy(result);
  }

  previous = parseFloat(current);
  operator = op;
  waitingForNext = true;
}

function equals() {
  if (!operator) return;

  const b = parseFloat(current);
  const result = calculate(previous, b, operator);
  if (result === null) return showError();

  expressionEl.textContent = `${formatNumber(String(previous))} ${SYMBOLS[operator]} ${formatNumber(String(b))} =`;
  current = tidy(result);
  previous = null;
  operator = null;
  waitingForNext = true;
}

function clearAll() {
  current = "0";
  previous = null;
  operator = null;
  waitingForNext = false;
  expressionEl.textContent = "";
}

function backspace() {
  if (waitingForNext) return;
  current = current.length > 1 ? current.slice(0, -1) : "0";
  if (current === "-") current = "0";
}

function toggleSign() {
  if (current === "0") return;
  current = current.startsWith("-") ? current.slice(1) : "-" + current;
}

function percent() {
  current = tidy(parseFloat(current) / 100);
}

function showError() {
  clearAll();
  errorMessage = "0으로 나눌 수 없음";
}

// ===== 화면 표시 =====
// 정수 부분에만 천 단위 쉼표를 넣는다 (입력 중인 "3." 같은 모양은 그대로 유지)
function formatNumber(text) {
  if (isNaN(parseFloat(text))) return text;
  const sign = text.startsWith("-") ? "-" : "";
  const [intPart, decPart] = text.replace(/^-/, "").split(".");
  const withComma = Number(intPart).toLocaleString("en-US");
  return decPart === undefined ? sign + withComma : `${sign}${withComma}.${decPart}`;
}

function render() {
  currentEl.textContent = errorMessage ?? formatNumber(current);
  currentEl.classList.toggle("small", currentEl.textContent.length > 10);

  // 계산 중일 때는 위쪽에 "12 +" 처럼 진행 중인 식을 보여주고,
  // 결과가 나온 뒤 새 숫자를 입력하기 시작하면 지운다
  if (operator) {
    expressionEl.textContent = `${formatNumber(String(previous))} ${SYMBOLS[operator]}`;
  } else if (!waitingForNext) {
    expressionEl.textContent = "";
  }

  // 선택된 연산자 버튼 강조
  document.querySelectorAll(".key.op").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.value === operator && waitingForNext);
  });
}

// ===== 버튼 / 키보드 연결 =====
function handleInput(value) {
  errorMessage = null; // 다음 입력이 오면 에러 문구는 지운다

  if (/^\d$/.test(value)) inputDigit(value);
  else if (value === ".") inputDot();
  else if (value in SYMBOLS) chooseOperator(value);
  else if (value === "equals") equals();
  else if (value === "clear") clearAll();
  else if (value === "backspace") backspace();
  else if (value === "sign") toggleSign();
  else if (value === "percent") percent();
  else return;

  render();
}

document.querySelector(".keys").addEventListener("click", (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;
  handleInput(btn.dataset.value ?? btn.dataset.action);
});

// 키보드 키 → 버튼 값
const KEY_MAP = {
  Enter: "equals", "=": "equals",
  Escape: "clear", Delete: "clear",
  Backspace: "backspace",
  "%": "percent",
};

document.addEventListener("keydown", (e) => {
  const value = KEY_MAP[e.key] ?? e.key;
  const btn = document.querySelector(`[data-value="${CSS.escape(value)}"], [data-action="${CSS.escape(value)}"]`);
  if (!btn) return;

  e.preventDefault();
  handleInput(value);

  // 키보드로 눌러도 버튼이 눌리는 효과
  btn.classList.add("pressed");
  setTimeout(() => btn.classList.remove("pressed"), 100);
});
