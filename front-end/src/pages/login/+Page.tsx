import React from 'react';

import { loginCheck } from '#root/utils/apis/login-queries';
import { LocalizedText } from '#root/utils/intl';

interface FormProps {
  onSubmit: (data: FormData) => void;
}

interface FormData {
  password: string;
  personalNumber: string;
}

export default function Login({ onSubmit }: FormProps) {
  const [formData, setFormData] = React.useState<FormData>({ password: '', personalNumber: '' });

  function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { value } = event.target;

    formData.personalNumber = value;
    setFormData({ ...formData });
  }

  function handlePasswordChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { value } = event.target;

    formData.password = value;
    setFormData({ ...formData });
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    loginCheck(formData.personalNumber, formData.password);
    event.preventDefault();
  }

  return (
    <>
      <section className="container flex min-h-screen flex-1 flex-col items-center justify-center">
        <form onSubmit={handleSubmit}>
          <label>
            <LocalizedText>Ange ditt personnummer</LocalizedText>
            <input
              type="text"
              name="name"
              required
              onChange={handleInputChange}
              placeholder="YYYYDDMM-XXXX"
            />
          </label>
          <label>
            <LocalizedText>Ange ditt losenord</LocalizedText>
            <input type="text" name="password" required onChange={handlePasswordChange} placeholder="XXXX" />
          </label>
          <br />
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
      </section>
    </>
  );
}
