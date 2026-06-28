const requiredChecks = [
  'تم تثبيت أدوات التطوير عبر pip install -e ".[dev]".',
  "نجح ruff check . دون أخطاء.",
  "نجح pytest على كامل حزمة الاختبارات.",
  "تمت مراجعة أن الخرج لا يمنح شهادة جاهزية بديلة عن أثر المستودع.",
  "البقايا والموانع المتبقية ظاهرة قبل إعلان الجاهزية.",
];

const checklist = document.querySelector("#checklist");
const readinessState = document.querySelector("#readiness-state");
const readinessDetail = document.querySelector("#readiness-detail");
const trialForm = document.querySelector("#trial-form");
const trialOutput = document.querySelector("#trial-output");

function renderChecklist() {
  requiredChecks.forEach((text, index) => {
    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    const span = document.createElement("span");

    checkbox.type = "checkbox";
    checkbox.dataset.checkIndex = String(index);
    span.textContent = text;
    label.append(checkbox, span);
    checklist.append(label);
  });
}

function updateReadiness() {
  const boxes = Array.from(checklist.querySelectorAll("input[type='checkbox']"));
  const completed = boxes.filter((box) => box.checked).length;
  const total = boxes.length;
  const ready = completed === total;

  readinessState.textContent = ready ? "جاهز للمراجعة المحلية" : "قيد المراجعة";
  readinessState.classList.toggle("ready", ready);
  readinessDetail.textContent = ready
    ? "كل عناصر الفحص معلّمة. شغّل الأوامر فعليًا قبل مشاركة النتيجة."
    : `اكتمل ${completed} من ${total} عناصر.`;
}

function collectResiduals(fields) {
  const residuals = [];

  if (!fields.question.trim()) {
    residuals.push("سؤال المستخدم غير ظاهر.");
  }
  if (!fields.answer.trim()) {
    residuals.push("جواب GPT غير ظاهر.");
  }
  if (!fields.evidence.trim()) {
    residuals.push("الدليل أو أصل المعرفة غير ظاهر.");
  }

  return residuals;
}

function buildEnvelope(fields) {
  const residuals = collectResiduals(fields);
  return {
    envelope: "TaaqolWebsiteTestEnvelope",
    scope: "local-static-review",
    questionVisible: Boolean(fields.question.trim()),
    answerVisible: Boolean(fields.answer.trim()),
    evidenceVisible: Boolean(fields.evidence.trim()),
    residualVisibility: true,
    residuals,
    verdict:
      residuals.length === 0
        ? "READY_FOR_REPOSITORY_TEST_COMMANDS"
        : "BLOCKED_BY_VISIBLE_RESIDUALS",
  };
}

renderChecklist();
updateReadiness();

checklist.addEventListener("change", updateReadiness);

trialForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const fields = {
    question: document.querySelector("#question").value,
    answer: document.querySelector("#answer").value,
    evidence: document.querySelector("#evidence").value,
  };
  const envelope = buildEnvelope(fields);

  trialOutput.textContent = JSON.stringify(envelope, null, 2);
});
