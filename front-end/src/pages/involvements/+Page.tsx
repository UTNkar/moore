export default function Involvement() {
  return (
    <>
      <div className="accordion" id="accordionExample">
        <h2 className="accordion-item accordion-header" id="headingOne">
          <button
            className="accordion-button"
            data-bs-toggle="collapse"
            data-bs-target="#multiCollapseExample1"
            type="button"
            aria-expanded="true"
            aria-controls="multiCollapseExample1"
          >
            Toggle first element
          </button>
        </h2>
        <div
          className="accordion-collapse show collapse"
          aria-labelledby="headingOne"
          id="multiCollapseExample1"
          data-bs-parent="#accordionExample"
        >
          <div className="accordion-body">
            Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid.
            Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident.
          </div>
        </div>
      </div>
    </>
  );
}
