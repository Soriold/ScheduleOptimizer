/* This example will only work in the latest browsers */
const initApp = () => {
  const registryToken = "78e99acc-a219-4b33-96bf-8175c84e5d19";

  const login = () => {
    Rosefire.signIn(registryToken, (err, rfUser) => {
      if (err) {
        return;
      }
      window.location.replace('/login?token=' + rfUser.token);
    });
  };
  const loginButton = document.getElementById('login');
  if (loginButton) {
    loginButton.onclick = login;
  }
}

window.onload = initApp;

