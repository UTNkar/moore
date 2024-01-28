import 'react-toastify/dist/ReactToastify.css';

export async function loginCheck(ssn: string, password: string): Promise<string> {
  const loginData = new FormData();

  loginData.append('username', ssn);
  loginData.append('password', password);
  loginData.append('next', '/');

  const login = await fetch('https://utn.se/accounts/login/', {
    body: loginData,
    method: 'POST',
  }).then((response) => response.json());

  return login;
}
