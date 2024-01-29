export async function loginCheck(username: string, password: string): Promise<string> {
  const loginData = new FormData();

  loginData.append('username', username);
  loginData.append('password', password);
  loginData.append('next', '/');

  const login = await fetch('https://utn.se/accounts/login/', {
    body: loginData,
    method: 'POST',
  }).then((response) => response.json());

  return login;
}
