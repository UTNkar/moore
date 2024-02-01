import React from 'react';

import { toast } from 'react-toastify';

import { ContactCard } from '#devlink';
import { membershipCheck } from '#root/utils/apis/membership-queries';
import { LocalizedText } from '#root/utils/intl';

interface FormProps {
  onSubmit: (data: FormData) => void;
}

interface FormData {
  personalNumber: string;
}

export default function MembershipCheck({ onSubmit }: FormProps) {
  const [formData, setFormData] = React.useState<FormData>({ personalNumber: '' });

  function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { value } = event.target;

    formData.personalNumber = value;
    setFormData({ ...formData });
  }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    if (membershipCheck(formData.personalNumber)) {
      toast('You are a member');
    } else {
      toast('You are not a member');
    }

    event.preventDefault();
  }

  return (
    <>
      <section className="container flex min-h-screen flex-1 flex-col items-center justify-center">
        <ContactCard name="Test" />
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
          <br />
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
      </section>
    </>
  );
}
