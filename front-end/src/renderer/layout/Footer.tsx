import Link from '#root/components/Link';
import LogoIcon from '#root/components/LogoIcon';
import { LocalizedText, useLocalizedText } from '#root/utils/intl';

export default function Footer() {
  return (
    <footer className="flex-0">
      <div className="py-12 md:py-16">
        <div className="container">
          <div className="mb-8 grid gap-8 md:mb-12 md:grid-cols-12 lg:gap-20">
            <div className="md:col-span-4 lg:col-span-5">
              <div className="mb-2">
                <Link
                  href="/"
                  className="inline-block"
                  aria-label={useLocalizedText('Uppsala teknolog- och naturvetarkår')}
                >
                  <LogoIcon className="h-10 w-10 fill-blue" />
                </Link>
              </div>
              <div className="text-gray-600">
                <LocalizedText>
                  Uppsala teknolog- och naturvetarkår är en studentkår för studenter på
                  teknisk-naturvetenskapliga fakulteten vid Uppsala universitet.
                </LocalizedText>{' '}
                <LocalizedText>Kontakta oss på</LocalizedText>{' '}
                <a className="font-semibold text-blue" href="mailto:admin@utn.se">
                  admin@utn.se
                </a>
                .
              </div>
            </div>
          </div>

          <div className="md:flex md:items-center md:justify-between">
            <div className="mr-4 text-gray-600">
              &copy; <LocalizedText>Uppsala teknolog- och naturvetarkår</LocalizedText>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
