import React, { useCallback } from 'react';
import { BASE_API_URL, REACT_APP_GOOGLE_CLIENT_ID } from 'src/constants';

function GoogleSSOButton() {
  const redirectToSSO = useCallback(() => {
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
    const redirectUri = '/api/v1/authenticate/google-oauth2';

    const scope = [
      'https://www.googleapis.com/auth/userinfo.email',
      'https://www.googleapis.com/auth/userinfo.profile',
      'openid',
    ].join(' ');

    const params = {
      response_type: 'code',
      client_id: REACT_APP_GOOGLE_CLIENT_ID,
      redirect_uri: `${BASE_API_URL}${redirectUri}`,
      prompt: 'select_account',
      access_type: 'offline',
      scope,
    };

    const urlParams = new URLSearchParams(params).toString();

    window.location.href = `${googleAuthUrl}?${urlParams}`;
  }, []);

  return (
    <div>
      <input
        type="image"
        onClick={redirectToSSO}
        src="../../../btn_google_signin_light_focus_web.png"
        alt="Sign in via Google SSO"
      />
    </div>
  );
}

export default GoogleSSOButton;
