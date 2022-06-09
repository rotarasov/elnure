import React, { useCallback } from 'react';
import redirectToGoogleSSO from 'src/api/sso';
import { BASE_API_URL, REACT_APP_GOOGLE_CLIENT_ID } from 'src/constants';

function GoogleSSOButton() {
  const redirectToSSO = useCallback(redirectToGoogleSSO, []);

  return (
    <div>
      <input
        type="image"
        onClick={() => redirectToSSO()}
        src="../../../btn_google_signin_light_focus_web.png"
        alt="Sign in via Google SSO"
      />
    </div>
  );
}

export default GoogleSSOButton;
