import {
  BASE_API_URL,
  BASE_FRONTEND_URL,
  REACT_APP_GOOGLE_CLIENT_ID,
} from "../constants";

export default function redirectToGoogleSSO(state: string = "") {
  const googleAuthUrl = "https://accounts.google.com/o/oauth2/v2/auth";
  const redirectUri = "/api/v1/authenticate/google-oauth2";

  const scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
  ].join(" ");

  state = state || `${BASE_FRONTEND_URL}/application-window`;

  const params = {
    response_type: "code",
    client_id: REACT_APP_GOOGLE_CLIENT_ID,
    redirect_uri: `${BASE_API_URL}${redirectUri}`,
    prompt: "select_account",
    access_type: "offline",
    state,
    scope,
  };

  const urlParams = new URLSearchParams(params).toString();

  window.location.href = `${googleAuthUrl}?${urlParams}`;
}
