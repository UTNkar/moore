import { LocalizedText } from '#root/utils/intl';

export default function HomePage() {
  return (
    <>
      <section className="container flex min-h-screen flex-1 flex-col items-center justify-center">
        <LocalizedText element="h1" className="h1">
          Uppsala teknolog- och naturvetarkår
        </LocalizedText>
      </section>
    </>
  );
}
