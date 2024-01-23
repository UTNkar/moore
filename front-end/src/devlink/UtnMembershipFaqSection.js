import React from 'react';

import * as _Builtin from './_Builtin';
import { FaqItem } from './FaqItem';

export function UtnMembershipFaqSection({
  as: _Component = _Builtin.Section,
  heading = 'Frågor och svar om UTN-medlemskap',
}) {
  return (
    <_Component
      className="section"
      grid={{
        type: 'section',
      }}
      tag="section"
    >
      <_Builtin.VFlex className="container" tag="div">
        <_Builtin.Heading tag="h2">{'Frågor och svar om UTN-medlemskap'}</_Builtin.Heading>
        <_Builtin.Block className="faq-list utn-membership" tag="div">
          <FaqItem
            question="Hur blir jag medlem i Uppsala teknolog- och naturvetarkår (UTN)?"
            answer={
              <>
                <_Builtin.Paragraph>
                  {
                    'Att bli medlem i UTN är enkelt och kostnadsfritt. Besök vår medlemskapssida, fyll i dina uppgifter och följ instruktionerna för att registrera dig.'
                  }
                </_Builtin.Paragraph>
                <_Builtin.Paragraph>{''}</_Builtin.Paragraph>
              </>
            }
          />
          <FaqItem
            answer={
              <>
                <_Builtin.Paragraph>
                  {
                    'Som medlem i UTN får du tillgång till rabatterade priser på evenemang och i vårt café, möjlighet att delta i Forsränningen och Rebusrallyt, tillgång till vår kårtidning Techna och veckovisa nyhetsbrev, samt möjligheten att engagera dig och påverka din studietid och studentliv.'
                  }
                </_Builtin.Paragraph>
                <_Builtin.Paragraph>{''}</_Builtin.Paragraph>
              </>
            }
            question="Vilka är fördelarna med att vara medlem i UTN?"
          />
          <FaqItem
            question="Är medlemskap i UTN ett krav för att engagera sig i kårens aktiviteter?"
            answer={
              <>
                <_Builtin.Paragraph>
                  {
                    'Ja, för att kunna engagera dig i kårens kommittéer, arbetsgrupper eller söka en arvoderad post behöver du vara medlem i UTN. Medlemskapet säkerställer även att du har rätt att rösta och påverka i kårens beslut.'
                  }
                </_Builtin.Paragraph>
                <_Builtin.Paragraph>{''}</_Builtin.Paragraph>
              </>
            }
          />
          <FaqItem
            question="Hur länge är medlemskapet i UTN giltigt?"
            answer={
              <>
                <_Builtin.Paragraph>
                  {
                    'Medlemskapet i UTN är giltigt under det läsår du registrerar dig. Du behöver förnya ditt medlemskap varje läsår för att fortsätta ta del av medlemsförmåner och för att behålla din röst i kårens beslut och val.'
                  }
                </_Builtin.Paragraph>
                <_Builtin.Paragraph>{''}</_Builtin.Paragraph>
              </>
            }
          />
        </_Builtin.Block>
      </_Builtin.VFlex>
    </_Component>
  );
}
