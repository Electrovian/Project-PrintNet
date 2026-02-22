export class FrontendContractError extends Error {
  constructor(code, detail) {
    super(String(detail || code || "frontend contract error"));
    this.name = "FrontendContractError";
    this.code = String(code || "FRONTEND_CONTRACT_ERROR");
  }
}

function asNonEmpty(value, field, code) {
  const text = String(value || "").trim();
  if (!text) {
    throw new FrontendContractError(code, `${field} is required.`);
  }
  return text;
}

export function normalizeContactPayload(payload) {
  const body = payload && typeof payload === "object" ? payload : {};
  const name = asNonEmpty(body.name, "name", "CONTACT_NAME_REQUIRED");
  const email = asNonEmpty(body.email, "email", "CONTACT_EMAIL_REQUIRED");
  const phone = asNonEmpty(body.phone, "phone", "CONTACT_PHONE_REQUIRED");
  if (!email.includes("@")) {
    throw new FrontendContractError("CONTACT_EMAIL_INVALID", "email must include '@'.");
  }
  return { name, email, phone };
}

export function normalizePrintRequestPayload(payload) {
  const body = payload && typeof payload === "object" ? payload : {};
  const modelName = asNonEmpty(body.modelName, "modelName", "MODEL_NAME_REQUIRED");
  const profileId = asNonEmpty(body.profileId, "profileId", "PROFILE_ID_REQUIRED");
  const requestedBy = asNonEmpty(body.requestedBy, "requestedBy", "REQUESTED_BY_REQUIRED");
  const printerId = String(body.printerId || "").trim();
  return { modelName, profileId, requestedBy, printerId };
}

export function normalizeModelUploadPayload(payload) {
  const body = payload && typeof payload === "object" ? payload : {};
  const fileName = asNonEmpty(body.fileName, "fileName", "MODEL_UPLOAD_FILE_NAME_REQUIRED");
  const dataBase64 = asNonEmpty(body.dataBase64, "dataBase64", "MODEL_UPLOAD_DATA_REQUIRED");
  return { fileName, dataBase64 };
}

export function normalizeSessionPayload(payload) {
  const body = payload && typeof payload === "object" ? payload : {};
  const userId = asNonEmpty(body.userId, "userId", "SESSION_USER_ID_REQUIRED");
  const role = String(body.role || "student").trim().toLowerCase() || "student";
  return { userId, role };
}

export function normalizePrinterRegistrationPayload(payload) {
  const body = payload && typeof payload === "object" ? payload : {};
  const printerId = asNonEmpty(body.printerId, "printerId", "PRINTER_ID_REQUIRED");
  const name = asNonEmpty(body.name, "name", "PRINTER_NAME_REQUIRED");
  const connectorType = asNonEmpty(body.connectorType, "connectorType", "PRINTER_CONNECTOR_REQUIRED").toLowerCase();
  const endpoint = asNonEmpty(body.endpoint, "endpoint", "PRINTER_ENDPOINT_REQUIRED");
  return { printerId, name, connectorType, endpoint };
}
