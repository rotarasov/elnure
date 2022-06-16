import React, { useCallback } from 'react';
import redirectToGoogleSSO from '../../api/sso';

function GoogleSSOButton() {
  const redirectToSSO = useCallback(redirectToGoogleSSO, []);

  return (
      <input
        type="image"
        onClick={() => redirectToSSO()}
        src="../../../btn_google_signin_light_focus_web.png"
        alt="Sign in via Google SSO"
      />
  );
}

export default GoogleSSOButton;
