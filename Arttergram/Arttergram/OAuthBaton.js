// JavaScript source code
const urlParams = new URLSearchParams(window.location.search);
OAuthToken = urlParams.get('oauth_token');
OAuthVerify = urlParams.get('oauth_verifier');
OAuthBaton = OAuthToken + "..." + OAuthVerify;
$.post('http://localhost:5656/batonpass', { OAuthBaton }, function () {
    window.location.replace("http://localhost:5656/shutdown");
})