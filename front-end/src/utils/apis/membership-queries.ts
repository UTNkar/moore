import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export async function membershipCheck(ssn: string): Promise<string> {
  const personnumber = new FormData();

  personnumber.append('ssn', ssn);

  const data = await fetch('https://utn.se/member_check_api/', {
    body: personnumber,
    method: 'POST',
  }).then((response) => response.json());

  if (data.is_member) {
    toast('You are a member');
  } else {
    toast('You are not a member');
  }

  return data.is_member;
}
