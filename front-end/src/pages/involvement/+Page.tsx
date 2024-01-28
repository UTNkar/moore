// import { usePositions } from '#root/api';
import { PageProps } from '#root/utils/page';

export default function InvolvementPage({ pageContext }: PageProps) {
  // const _positions = usePositions();

  return (
    <>
      <div className="sticky-content-sidebar involvement" />
      <div className="sticky-content-body involvement-module">
        <div className="module-item-header" />

        <div className="divider involvement-content" />
      </div>
    </>
  );
}
