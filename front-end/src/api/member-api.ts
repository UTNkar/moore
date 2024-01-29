export async function checkMembership(ssn: string): Promise<boolean> {
  const body = new FormData();

  body.append('ssn', ssn);

  const data = await fetch('https://utn.se/member_check_api/', {
    body,
    method: 'POST',
  }).then((response) => response.json());

  return data.is_member;
}
