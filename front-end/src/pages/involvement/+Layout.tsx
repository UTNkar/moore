import Container from '#root/components/Container';
import NavigationButtonGroup from '#root/components/NavigationButtonGroup';
import Section from '#root/components/Section';
import Tabs from '#root/components/Tabs';
import DefaultLayout from '#root/renderer/layout/DefaultLayout';
import { LocalizedText } from '#root/utils/intl';
import { LayoutProps, isWithinIframe } from '#root/utils/page';

export default function InvolvementLayout({ children, pageContext }: LayoutProps) {
  const iframeContent = (
    <div className="w-layout-hflex sticky-content-wrapper involvement">
      <Tabs
        tabs={[
          {
            children: <LocalizedText element="span">Lediga poster</LocalizedText>,
            href: '/involvement',
          },
          {
            children: <LocalizedText element="span">Sökta poster</LocalizedText>,
            href: '/involvement/applications',
          },
          'space',
          {
            children: <LocalizedText element="span">Min profil</LocalizedText>,
            href: '/involvement/profile',
          },
        ]}
      />

      {children}
    </div>
  );

  if (isWithinIframe(pageContext)) {
    return iframeContent;
  }

  return (
    <DefaultLayout pageContext={pageContext}>
      <Section>
        <Container>
          <LocalizedText element="h1">Engagemang</LocalizedText>

          <p className="large-paragraph">
            <LocalizedText element="span">Här kan du använda modulen som finns på</LocalizedText>
            &nbsp;
            <a href="https://utn.se/event">utn.se/engagemang</a>.
          </p>

          <NavigationButtonGroup exclude="involvement" />
        </Container>
      </Section>

      <Section subdued emphasised>
        <Container>{iframeContent}</Container>
      </Section>
    </DefaultLayout>
  );
}
