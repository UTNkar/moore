import { LocalizedText } from '#root/utils/intl';

export default Page;

function Page({ is404 }: any) {
  let content: JSX.Element;

  if (is404) {
    content = (
      <>
        <LocalizedText element="h1" className="h1">
          404
        </LocalizedText>
        <LocalizedText element="p" className="mt-4 text-xl">
          Den här sidan kunde inte hittas.
        </LocalizedText>
        <LocalizedText element="p" className="text-xl">
          Vi ber om ursäkt för det.
        </LocalizedText>
      </>
    );
  } else {
    content = (
      <>
        <LocalizedText element="h1" className="h1">
          500 Internt fel
        </LocalizedText>
        <LocalizedText element="p" className="mt-4 text-xl">
          Något gick snett.
        </LocalizedText>
        <LocalizedText element="p" className="text-xl">
          Vi ber om ursäkt för det.
        </LocalizedText>
      </>
    );
  }

  return (
    <section>
      <div className="relative mx-auto max-w-6xl px-4 py-24 sm:px-6 md:py-32">{content}</div>
    </section>
  );
}
