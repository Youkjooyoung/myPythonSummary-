// ===== 계산기 상태 =====
let current = "0";          // 지금 화면에 입력 중인 숫자 (문자열)
let previous = null;        // 연산자 앞의 숫자
let operator = null;        // 선택한 연산자 (+, -, *, /)
let waitingForNext = false; // 연산자나 = 을 누른 직후인지 (다음 숫자를 새로 입력해야 함)
let replaceOnInput = false; // 기록에서 불러온 값인지 (숫자를 누르면 이어 붙이지 않고 새로 입력)
let errorMessage = null;    // 에러가 나면 화면에 잠깐 띄울 문구

const MAX_LENGTH = 15;
const MAX_HISTORY = 50;
const STORAGE_KEY = "calculator-history";
const SYMBOLS = { "+": "+", "-": "−", "*": "×", "/": "÷" };

const expressionEl = document.getElementById("expression");
const currentEl = document.getElementById("current");
const historyListEl = document.getElementById("history-list");
const historyEmptyEl = document.getElementById("history-empty");

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
  if (waitingForNext || replaceOnInput) {
    current = digit;
    waitingForNext = false;
    replaceOnInput = false;
  } else if (current.replace(/[-.]/g, "").length < MAX_LENGTH) {
    current = current === "0" ? digit : current + digit;
  }
}

function inputDot() {
  if (waitingForNext || replaceOnInput) {
    current = "0.";
    waitingForNext = false;
    replaceOnInput = false;
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
  replaceOnInput = false;
}

function equals() {
  if (!operator) return;

  const b = parseFloat(current);
  const result = calculate(previous, b, operator);
  if (result === null) return showError();

  const expression = `${formatNumber(String(previous))} ${SYMBOLS[operator]} ${formatNumber(String(b))}`;
  expressionEl.textContent = `${expression} =`;
  current = tidy(result);
  addHistory(expression, current);

  previous = null;
  operator = null;
  waitingForNext = true;
  replaceOnInput = false;
}

function clearAll() {
  current = "0";
  previous = null;
  operator = null;
  waitingForNext = false;
  replaceOnInput = false;
  expressionEl.textContent = "";
}

function backspace() {
  if (waitingForNext || replaceOnInput) return;
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

// ===== 계산 기록 =====
// 저장소를 못 쓰는 환경(시크릿 창 등)에서도 계산기는 동작하도록 try/catch로 감싼다
function loadHistory() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    return Array.isArray(saved) ? saved : [];
  } catch {
    return [];
  }
}

function saveHistory() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(historyItems));
  } catch {
    // 저장 실패는 무시 (이번 접속 동안만 기록이 유지됨)
  }
}

let historyItems = loadHistory(); // [{ expression: "12 × 3", result: "36" }, ...] 최신이 맨 앞

function addHistory(expression, result) {
  historyItems.unshift({ expression, result });
  historyItems = historyItems.slice(0, MAX_HISTORY);
  saveHistory();
  renderHistory();
}

function clearHistory() {
  historyItems = [];
  saveHistory();
  renderHistory();
}

// 기록의 결과값을 불러온다. 연산자를 고른 뒤라면 두 번째 숫자로, 아니면 새 계산의 첫 숫자로 쓰인다
function useHistory(index) {
  current = historyItems[index].result;
  waitingForNext = false;
  replaceOnInput = true;
  errorMessage = null;
  render();
}

function renderHistory() {
  historyListEl.innerHTML = "";
  historyEmptyEl.hidden = historyItems.length > 0;

  historyItems.forEach((item, index) => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.className = "history-item";
    btn.dataset.index = index;

    // 저장소에서 읽은 값이라 innerHTML 대신 textContent로 넣는다
    const expr = document.createElement("span");
    expr.className = "history-expr";
    expr.textContent = `${item.expression} =`;

    const result = document.createElement("span");
    result.className = "history-result";
    result.textContent = formatNumber(item.result);

    btn.append(expr, result);
    li.append(btn);
    historyListEl.append(li);
  });
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

const keysEl = document.querySelector(".keys");

keysEl.addEventListener("click", (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;
  handleInput(btn.dataset.value ?? btn.dataset.action);
});

historyListEl.addEventListener("click", (e) => {
  const btn = e.target.closest(".history-item");
  if (!btn) return;
  useHistory(Number(btn.dataset.index));
});

document.getElementById("clear-history").addEventListener("click", clearHistory);

// 키보드 키 → 버튼 값
const KEY_MAP = {
  Enter: "equals", "=": "equals",
  Escape: "clear", Delete: "clear",
  Backspace: "backspace",
  "%": "percent",
};

document.addEventListener("keydown", (e) => {
  const value = KEY_MAP[e.key] ?? e.key;
  const btn = keysEl.querySelector(`[data-value="${CSS.escape(value)}"], [data-action="${CSS.escape(value)}"]`);
  if (!btn) return;

  e.preventDefault(); // 버튼에 포커스가 있을 때 Enter가 클릭으로 한 번 더 눌리는 것을 막는다
  handleInput(value);

  // 키보드로 눌러도 버튼이 눌리는 효과
  btn.classList.add("pressed");
  setTimeout(() => btn.classList.remove("pressed"), 100);
});

renderHistory();
