// ===== 공통: 설정 저장 =====
const THEME_KEY = "life-calc-theme";
const TAB_KEY = "life-calc-tab";

// 개인 창이나 저장소가 막힌 브라우저에서는 localStorage가 에러를 내므로 감싸서 쓴다
function loadSetting(key) {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function saveSetting(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch {
    // 저장하지 못해도 계산기는 그대로 쓸 수 있다
  }
}

// ===== 공통: 입력 읽기와 결과 출력 =====
function inputValue(id) {
  return document.getElementById(id).value;
}

// "12,000" 처럼 쉼표가 있어도 숫자로 바꾼다. 빈 칸은 null, 숫자가 아니면 NaN
function numberOf(id) {
  const cleaned = inputValue(id).replace(/,/g, "").trim();
  return cleaned === "" ? null : Number(cleaned);
}

function checkedValue(name) {
  return document.querySelector(`input[name="${name}"]:checked`).value;
}

function won(n) {
  return Math.round(n).toLocaleString("ko-KR") + "원";
}

function decimal(n, digits = 2) {
  return n.toLocaleString("ko-KR", { maximumFractionDigits: digits });
}

// 결과 영역에 [이름, 값, 강조 여부] 행을 그린다
function showResult(el, rows) {
  el.replaceChildren(...rows.map(([label, value, isMain]) => {
    const row = document.createElement("div");
    row.className = isMain ? "result-row main" : "result-row";
    const name = document.createElement("span");
    name.textContent = label;
    const val = document.createElement("strong");
    val.textContent = value;
    row.append(name, val);
    return row;
  }));
}

// 입력이 비었거나 잘못됐을 때 결과 대신 안내 문구를 보여준다
function showHint(el, text) {
  const p = document.createElement("p");
  p.className = "hint";
  p.textContent = text;
  el.replaceChildren(p);
}

// 금액 칸은 입력을 마치면(포커스가 빠지면) 쉼표를 넣어 보기 좋게 바꾼다
document.querySelectorAll("input[data-money]").forEach((input) => {
  input.addEventListener("blur", () => {
    const n = numberOf(input.id);
    if (Number.isFinite(n)) input.value = Math.round(n).toLocaleString("ko-KR");
  });
});

// ===== 테마 =====
const themeBtn = document.getElementById("theme-toggle");

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeBtn.textContent = theme === "dark" ? "☀️" : "🌙";
  themeBtn.setAttribute("aria-label", theme === "dark" ? "라이트 모드로 전환" : "다크 모드로 전환");
}

// 저장된 선택이 없으면 OS 설정을 따른다
const savedTheme = loadSetting(THEME_KEY);
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
applyTheme(savedTheme === "dark" || savedTheme === "light" ? savedTheme : prefersDark ? "dark" : "light");

themeBtn.addEventListener("click", () => {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(next);
  saveSetting(THEME_KEY, next);
});

// ===== 탭 =====
const tabButtons = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".panel");
let activeTab = "basic";

function showTab(name) {
  activeTab = name;
  tabButtons.forEach((btn) => {
    const selected = btn.dataset.tab === name;
    btn.classList.toggle("active", selected);
    btn.setAttribute("aria-selected", selected);
  });
  panels.forEach((panel) => {
    panel.hidden = panel.dataset.panel !== name;
  });
  saveSetting(TAB_KEY, name);
}

tabButtons.forEach((btn) => {
  btn.addEventListener("click", () => showTab(btn.dataset.tab));
});

// ===== 1. 기본 계산기 =====
let tokens = [];              // 지금까지 입력한 식: ["2", "+", "3", "*"]
let current = "0";            // 지금 입력 중인 숫자 (문자열)
let waitingForNumber = false; // 연산자를 누른 직후인지 (다음 숫자를 새로 입력해야 함)
let justEvaluated = false;    // = 을 누른 직후인지
let lastExpression = "";      // = 을 누른 뒤 위쪽에 보여줄 식
let errorMessage = null;      // 에러가 나면 화면에 띄울 문구

const MAX_DIGITS = 15;
const SYMBOLS = { "+": "+", "-": "−", "*": "×", "/": "÷" };

const expressionEl = document.getElementById("expression");
const currentEl = document.getElementById("current");

// 0.1 + 0.2 = 0.30000000000000004 같은 소수 오차를 정리
function tidy(num) {
  return String(parseFloat(num.toPrecision(12)));
}

// 곱셈·나눗셈을 먼저 계산한 뒤 덧셈·뺄셈을 왼쪽부터 계산한다 (eval 사용 안 함)
function evaluate(list) {
  // 1단계: ×, ÷ 를 계산해서 [숫자, +/-, 숫자, ...] 만 남긴다
  const sums = [Number(list[0])];
  for (let i = 1; i < list.length; i += 2) {
    const op = list[i];
    const num = Number(list[i + 1]);
    if (op === "*") {
      sums.push(sums.pop() * num);
    } else if (op === "/") {
      if (num === 0) return null; // 0으로 나누기는 null로 표시
      sums.push(sums.pop() / num);
    } else {
      sums.push(op, num);
    }
  }

  // 2단계: +, - 를 왼쪽부터 계산
  let result = sums[0];
  for (let i = 1; i < sums.length; i += 2) {
    result = sums[i] === "+" ? result + sums[i + 1] : result - sums[i + 1];
  }
  return result;
}

// "1234567.5" → "1,234,567.5" (소수점 아래는 그대로)
function formatDisplay(str) {
  if (str.includes("e")) return str;
  const [intPart, decPart] = str.split(".");
  const withCommas = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return decPart === undefined ? withCommas : withCommas + "." + decPart;
}

function expressionText(list) {
  return list.map((t) => SYMBOLS[t] ?? formatDisplay(String(Number(t)))).join(" ");
}

function renderBasic() {
  expressionEl.textContent = justEvaluated ? lastExpression : expressionText(tokens);
  currentEl.textContent = errorMessage ?? formatDisplay(current);
  currentEl.classList.toggle("error", errorMessage !== null);
  currentEl.classList.toggle("long", errorMessage === null && current.length > 12);
}

function resetBasic() {
  tokens = [];
  current = "0";
  waitingForNumber = false;
  justEvaluated = false;
  lastExpression = "";
  errorMessage = null;
}

// 에러가 난 뒤나 = 을 누른 뒤에 숫자를 누르면 처음부터 새로 시작
function startFresh() {
  if (errorMessage !== null || justEvaluated) resetBasic();
}

function inputDigit(digit) {
  startFresh();
  if (waitingForNumber) {
    current = digit;
    waitingForNumber = false;
  } else if (current === "0") {
    current = digit;
  } else if (current === "-0") {
    current = "-" + digit;
  } else if (current.replace(/[-.]/g, "").length < MAX_DIGITS) {
    current += digit;
  }
}

function inputDot() {
  startFresh();
  if (waitingForNumber) {
    current = "0.";
    waitingForNumber = false;
  } else if (!current.includes(".")) {
    current += ".";
  }
}

function inputOperator(op) {
  if (errorMessage !== null) return;
  justEvaluated = false; // = 직후라면 그 결과에 이어서 계산
  if (waitingForNumber) {
    tokens[tokens.length - 1] = op; // 연산자를 연달아 누르면 마지막 것으로 바꾼다
  } else {
    tokens.push(current, op);
    waitingForNumber = true;
  }
}

function equals() {
  if (errorMessage !== null || tokens.length === 0) return;
  // "5 +" 처럼 연산자로 끝나면 마지막 연산자는 버린다
  const list = waitingForNumber ? tokens.slice(0, -1) : [...tokens, current];
  const result = evaluate(list);

  lastExpression = expressionText(list) + " =";
  tokens = [];
  waitingForNumber = false;
  justEvaluated = true;

  if (result === null) {
    errorMessage = "0으로 나눌 수 없습니다";
  } else if (!Number.isFinite(result)) {
    errorMessage = "계산 범위를 벗어났습니다";
  } else {
    current = tidy(result);
  }
}

function percent() {
  if (errorMessage !== null || waitingForNumber) return;
  current = tidy(Number(current) / 100);
}

function toggleSign() {
  if (errorMessage !== null) return;
  if (waitingForNumber) {
    current = "-0"; // 연산자 다음에 누르면 음수를 새로 입력
    waitingForNumber = false;
  } else {
    current = current.startsWith("-") ? current.slice(1) : "-" + current;
  }
}

function backspace() {
  if (errorMessage !== null) {
    resetBasic();
  } else if (justEvaluated) {
    lastExpression = ""; // 결과는 남기고 위쪽 식만 지운다
  } else if (!waitingForNumber) {
    current = current.slice(0, -1);
    if (current === "" || current === "-") current = "0";
  }
}

function pressKey(key) {
  if (/^\d$/.test(key)) inputDigit(key);
  else if (key === ".") inputDot();
  else if (key in SYMBOLS) inputOperator(key);
  else if (key === "=") equals();
  else if (key === "clear") resetBasic();
  else if (key === "backspace") backspace();
  else if (key === "percent") percent();
  else if (key === "sign") toggleSign();
  renderBasic();
}

document.querySelector(".keys").addEventListener("click", (e) => {
  const btn = e.target.closest(".key");
  if (btn) pressKey(btn.dataset.key);
});

// 키보드: 계산기 탭이 열려 있고, 다른 입력 칸에 커서가 없을 때만 받는다
const KEY_MAP = { Enter: "=", "=": "=", Backspace: "backspace", Escape: "clear", Delete: "clear", "%": "percent" };

document.addEventListener("keydown", (e) => {
  if (activeTab !== "basic" || e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.target.closest("input, select, textarea")) return;
  const key = KEY_MAP[e.key] ?? e.key;
  if (!/^[\d.+\-*/]$/.test(key) && !(e.key in KEY_MAP)) return;
  e.preventDefault(); // 포커스된 버튼이 Enter로 한 번 더 눌리는 것을 막는다
  pressKey(key);
});

// ===== 2. 할인 =====
function isRate(n) {
  return Number.isFinite(n) && n >= 0 && n <= 100;
}

function calcDiscount() {
  const el = document.getElementById("discount-result");
  const price = numberOf("discount-price");
  const rate1 = numberOf("discount-rate1");
  const rate2 = numberOf("discount-rate2") ?? 0; // 추가 할인은 비워 둬도 된다

  if (price === null || rate1 === null) return showHint(el, "정가와 할인율을 입력하세요.");
  if (!(price > 0)) return showHint(el, "정가는 0보다 큰 숫자로 입력하세요.");
  if (!isRate(rate1) || !isRate(rate2)) return showHint(el, "할인율은 0~100 사이로 입력하세요.");

  const final = Math.round(price * (1 - rate1 / 100) * (1 - rate2 / 100));
  const saved = price - final;
  showResult(el, [
    ["할인가", won(final), true],
    ["절약 금액", won(saved)],
    ["실제 총 할인율", decimal((saved / price) * 100) + "%"],
  ]);
}

// ===== 3. 더치페이·팁 =====
function calcDutch() {
  const el = document.getElementById("dutch-result");
  const total = numberOf("dutch-total");
  const people = numberOf("dutch-people");
  const tip = numberOf("dutch-tip") ?? 0;
  const unit = Number(inputValue("dutch-unit"));

  if (total === null || people === null) return showHint(el, "총액과 인원을 입력하세요.");
  if (!(total > 0)) return showHint(el, "총액은 0보다 큰 숫자로 입력하세요.");
  if (!Number.isInteger(people) || people < 1) return showHint(el, "인원은 1명 이상의 정수로 입력하세요.");
  if (!(tip >= 0)) return showHint(el, "팁은 0% 이상으로 입력하세요.");

  const tipAmount = Math.round((total * tip) / 100);
  const pay = Math.round(total) + tipAmount;
  const perPerson = Math.ceil(pay / people / unit) * unit; // 고른 단위로 올림
  const collected = perPerson * people;

  const rows = [["1인당", won(perPerson), true]];
  if (tipAmount > 0) rows.push(["팁 금액", won(tipAmount)]);
  rows.push(
    ["결제할 금액", won(pay)],
    ["걷는 금액 합계", won(collected)],
    ["올림으로 남는 돈", won(collected - pay)],
  );
  showResult(el, rows);
}

// ===== 4. 예적금 이자 =====
// 금리는 % 그대로(3 = 3%) 받아서 마지막에 1200(=100%×12개월)으로 나눈다. 0.03/12 같은 소수 오차를 줄이기 위해
// 예금: 처음 넣은 원금에 n개월 동안 이자가 붙는다
function depositInterest(principal, ratePercent, months, method) {
  if (method === "simple") return (principal * ratePercent * months) / 1200;
  return principal * ((1 + ratePercent / 1200) ** months - 1);
}

// 적금: 매달 넣은 돈마다 남은 개월 수만큼 이자가 붙는다 (첫 달 돈은 n개월, 마지막 달 돈은 1개월)
function installmentInterest(monthly, ratePercent, months, method) {
  if (method === "simple") return (monthly * ratePercent * months * (months + 1)) / 2 / 1200;
  let sum = 0;
  for (let k = 1; k <= months; k++) {
    sum += monthly * ((1 + ratePercent / 1200) ** k - 1);
  }
  return sum;
}

function calcSaving() {
  const el = document.getElementById("saving-result");
  const type = checkedValue("saving-type"); // deposit(예금) / installment(적금)
  document.getElementById("saving-amount-label").textContent = type === "deposit" ? "예치 금액" : "월 납입액";

  const amount = numberOf("saving-amount");
  const ratePercent = numberOf("saving-rate");
  const months = numberOf("saving-months");
  const method = checkedValue("saving-method");
  const taxPermil = Number(inputValue("saving-tax")); // 천분율: 154 = 15.4%

  if (amount === null || ratePercent === null || months === null) return showHint(el, "금액, 연이율, 기간을 모두 입력하세요.");
  if (!(amount > 0)) return showHint(el, "금액은 0보다 큰 숫자로 입력하세요.");
  if (!isRate(ratePercent)) return showHint(el, "연이율은 0~100% 사이로 입력하세요.");
  if (!Number.isInteger(months) || months < 1 || months > 600) return showHint(el, "기간은 1~600개월 사이의 정수로 입력하세요.");

  const rawInterest = type === "deposit"
    ? depositInterest(amount, ratePercent, months, method)
    : installmentInterest(amount, ratePercent, months, method);
  const interest = Math.floor(rawInterest + 1e-6); // 원 단위 미만 버림 (0.9999… 같은 오차는 보정)
  const tax = Math.floor((interest * taxPermil) / 1000);
  const principal = Math.round(type === "deposit" ? amount : amount * months);

  showResult(el, [
    ["세후 수령액", won(principal + interest - tax), true],
    ["원금 합계", won(principal)],
    ["세전 이자", won(interest)],
    [`이자 과세 (${decimal(taxPermil / 10, 1)}%)`, "−" + won(tax)],
    ["세후 이자", won(interest - tax)],
  ]);
}

// ===== 5. 단위 변환 =====
// 길이는 m, 무게는 g, 넓이는 ㎡ 를 기준으로 몇 배인지 적어 둔다. 온도는 배율이 아니라 공식으로 바꾼다
const UNITS = {
  length: {
    defaults: ["cm", "in"],
    units: {
      mm: ["mm (밀리미터)", 0.001],
      cm: ["cm (센티미터)", 0.01],
      m: ["m (미터)", 1],
      km: ["km (킬로미터)", 1000],
      in: ["in (인치)", 0.0254],
      ft: ["ft (피트)", 0.3048],
      yd: ["yd (야드)", 0.9144],
      mile: ["mile (마일)", 1609.344],
    },
  },
  weight: {
    defaults: ["kg", "lb"],
    units: {
      g: ["g (그램)", 1],
      kg: ["kg (킬로그램)", 1000],
      t: ["t (톤)", 1000000],
      oz: ["oz (온스)", 28.349523125],
      lb: ["lb (파운드)", 453.59237],
      geun: ["근 (600g)", 600],
    },
  },
  temperature: {
    defaults: ["C", "F"],
    units: {
      C: ["°C (섭씨)"],
      F: ["°F (화씨)"],
      K: ["K (켈빈)"],
    },
  },
  area: {
    defaults: ["pyeong", "m2"],
    units: {
      m2: ["㎡ (제곱미터)", 1],
      pyeong: ["평", 3.305785],
      a: ["a (아르)", 100],
      ha: ["ha (헥타르)", 10000],
    },
  },
};

const unitCategoryEl = document.getElementById("unit-category");
const unitFromEl = document.getElementById("unit-from");
const unitToEl = document.getElementById("unit-to");

function toCelsius(value, unit) {
  if (unit === "F") return ((value - 32) * 5) / 9;
  if (unit === "K") return value - 273.15;
  return value;
}

function fromCelsius(celsius, unit) {
  if (unit === "F") return (celsius * 9) / 5 + 32;
  if (unit === "K") return celsius + 273.15;
  return celsius;
}

// 분류를 바꾸면 단위 목록을 새로 채우고 기본 단위를 고른다
function fillUnitOptions() {
  const { defaults, units } = UNITS[unitCategoryEl.value];
  [unitFromEl, unitToEl].forEach((select, i) => {
    select.replaceChildren(...Object.entries(units).map(([key, [label]]) => new Option(label, key)));
    select.value = defaults[i];
  });
}

function calcUnit() {
  const el = document.getElementById("unit-result");
  const category = unitCategoryEl.value;
  const value = numberOf("unit-value");
  const from = unitFromEl.value;
  const to = unitToEl.value;
  const units = UNITS[category].units;

  if (value === null) return showHint(el, "변환할 값을 입력하세요.");
  if (!Number.isFinite(value)) return showHint(el, "숫자로 입력하세요.");

  let result;
  if (category === "temperature") {
    const celsius = toCelsius(value, from);
    if (celsius < -273.15) return showHint(el, "절대영도(−273.15°C)보다 낮을 수 없습니다.");
    result = fromCelsius(celsius, to);
  } else {
    if (value < 0) return showHint(el, "0 이상의 값을 입력하세요.");
    result = (value * units[from][1]) / units[to][1];
  }

  // 단위 이름에서 괄호 앞 기호만 쓴다: "cm (센티미터)" → "cm"
  const symbol = (key) => units[key][0].split(" (")[0];
  const formatted = parseFloat(result.toPrecision(10)).toLocaleString("ko-KR", { maximumSignificantDigits: 10 });
  showResult(el, [[`${decimal(value, 10)} ${symbol(from)} =`, `${formatted} ${symbol(to)}`, true]]);
}

document.getElementById("unit-swap").addEventListener("click", () => {
  [unitFromEl.value, unitToEl.value] = [unitToEl.value, unitFromEl.value];
  calcUnit();
});

// ===== 6. 날짜 =====
const DAY = 24 * 60 * 60 * 1000;
const WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"];

// "2026-10-23" → UTC 기준 밀리초. 시간대·서머타임 때문에 하루가 23시간이 되는 오차를 피한다
function parseDate(value) {
  if (!value) return null;
  const [y, m, d] = value.split("-").map(Number);
  return Date.UTC(y, m - 1, d);
}

function todayUTC() {
  const now = new Date();
  return Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
}

// 날짜 입력 칸의 기본값으로 쓸 오늘 날짜 문자열 "2026-10-23"
function todayString() {
  return new Date(todayUTC()).toISOString().slice(0, 10);
}

function formatDate(ms) {
  const d = new Date(ms);
  return `${d.getUTCFullYear()}년 ${d.getUTCMonth() + 1}월 ${d.getUTCDate()}일 (${WEEKDAYS[d.getUTCDay()]})`;
}

function daysBetween(from, to) {
  return Math.round((to - from) / DAY);
}

function calcDate() {
  const el = document.getElementById("date-result");
  const mode = checkedValue("date-mode"); // dday / between / add

  // 고른 계산 종류에 맞는 입력 칸만 보여준다
  document.querySelectorAll("[data-date-mode]").forEach((group) => {
    group.hidden = group.dataset.dateMode !== mode;
  });
  document.getElementById("date-include-wrap").hidden = mode === "dday";
  const include = document.getElementById("date-include").checked ? 1 : 0;

  if (mode === "dday") {
    const target = parseDate(inputValue("date-target"));
    if (target === null) return showHint(el, "목표일을 선택하세요.");
    const today = todayUTC();
    const diff = daysBetween(today, target);
    const label = diff === 0 ? "D-Day" : diff > 0 ? `D-${diff}` : `D+${-diff}`;
    showResult(el, [
      ["D-day", label, true],
      ["목표일", formatDate(target)],
      ["오늘", formatDate(today)],
    ]);
  } else if (mode === "between") {
    const start = parseDate(inputValue("date-start"));
    const end = parseDate(inputValue("date-end"));
    if (start === null || end === null) return showHint(el, "시작일과 종료일을 선택하세요.");
    const diff = daysBetween(start, end);
    if (diff < 0) return showHint(el, "종료일이 시작일보다 빠릅니다.");
    const days = diff + include;
    showResult(el, [
      ["기간", `${days.toLocaleString("ko-KR")}일`, true],
      ["주 단위", `${Math.floor(days / 7)}주 ${days % 7}일`],
    ]);
  } else {
    const base = parseDate(inputValue("date-base"));
    const days = numberOf("date-days");
    if (base === null || days === null) return showHint(el, "기준일과 일수를 입력하세요.");
    if (!Number.isInteger(days) || days < 0) return showHint(el, "일수는 0 이상의 정수로 입력하세요.");
    // 시작일을 1일로 세면 100일째 되는 날은 기준일 + 99일
    const offset = Math.max(days - include, 0);
    const sign = inputValue("date-direction") === "after" ? 1 : -1;
    showResult(el, [
      ["결과", formatDate(base + sign * offset * DAY), true],
      ["기준일", formatDate(base)],
    ]);
  }
}

// ===== 7. 나이 =====
function isLeapYear(year) {
  return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
}

// 그해의 생일. 2월 29일생은 평년에 3월 1일을 생일로 본다
function birthdayIn(year, month, day) {
  if (month === 2 && day === 29 && !isLeapYear(year)) return Date.UTC(year, 2, 1);
  return Date.UTC(year, month - 1, day);
}

function calcAge() {
  const el = document.getElementById("age-result");
  const birth = parseDate(inputValue("age-birth"));
  const base = parseDate(inputValue("age-base")) ?? todayUTC();

  if (birth === null) return showHint(el, "생년월일을 선택하세요.");
  if (birth > base) return showHint(el, "생년월일이 기준일보다 늦습니다.");

  const b = new Date(birth);
  const t = new Date(base);
  const birthYear = b.getUTCFullYear();
  const birthMonth = b.getUTCMonth() + 1;
  const birthDay = b.getUTCDate();
  const baseYear = t.getUTCFullYear();

  // 올해 생일이 아직 안 지났으면 한 살 뺀다
  const passed = base >= birthdayIn(baseYear, birthMonth, birthDay);
  const manAge = baseYear - birthYear - (passed ? 0 : 1);
  const yearAge = baseYear - birthYear;

  let next = birthdayIn(baseYear, birthMonth, birthDay);
  if (next < base) next = birthdayIn(baseYear + 1, birthMonth, birthDay);
  const daysLeft = daysBetween(base, next);

  showResult(el, [
    ["만 나이", `${manAge}세`, true],
    ["연 나이", `${yearAge}세`],
    ["다음 생일", daysLeft === 0 ? "오늘이 생일 🎂" : `${formatDate(next)} · D-${daysLeft}`],
    ["태어난 지", `${(daysBetween(birth, base) + 1).toLocaleString("ko-KR")}일째`],
  ]);
}

// ===== 시작 =====
// 입력이 바뀔 때마다 해당 탭을 바로 다시 계산한다
const calculators = { discount: calcDiscount, dutch: calcDutch, saving: calcSaving, date: calcDate, age: calcAge };
Object.entries(calculators).forEach(([name, calc]) => {
  document.querySelector(`[data-panel="${name}"]`).addEventListener("input", calc);
});

document.querySelector('[data-panel="unit"]').addEventListener("input", (e) => {
  if (e.target === unitCategoryEl) fillUnitOptions();
  calcUnit();
});

// 날짜 칸 기본값은 오늘
["date-start", "date-base", "age-base"].forEach((id) => {
  document.getElementById(id).value = todayString();
});

fillUnitOptions();
Object.values(calculators).forEach((calc) => calc());
calcUnit();
renderBasic();

// 마지막으로 보던 탭을 연다
const savedTab = loadSetting(TAB_KEY);
showTab([...tabButtons].some((btn) => btn.dataset.tab === savedTab) ? savedTab : "basic");
