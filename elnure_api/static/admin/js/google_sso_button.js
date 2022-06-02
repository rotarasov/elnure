function googleSSOOnClick(googleClientId, baseApiUrl) {
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
    const redirectUri = '/api/v1/authenticate/google-oauth2';

    const scope = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid',
    ].join(' ');


    let next = '/admin/'
    for (let element of window.location.search.substring(1).split('&')) {
        if (element.includes('next=')) {
            next = element.split('=')[1]
            break
        }
    }

    const params = {
        response_type: 'code',
        client_id: googleClientId,
        redirect_uri: `${baseApiUrl}${redirectUri}`,
        prompt: 'select_account',
        access_type: 'offline',
        state: `${baseApiUrl}${next}`,
        scope,
    };

    const urlParams = new URLSearchParams(params).toString();

    window.location.href = `${googleAuthUrl}?${urlParams}`;
}