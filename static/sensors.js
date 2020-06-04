setInterval(async () => {
  let req = await fetch("http://127.0.0.1:5000/api/motion", {
    mode: "cors",
  });
  let res = await req.json();
  if (res.movement === 1) {
    const toastContainer = document.getElementById("toasts-container");
    toastContainer.innerHTML = "";
    let $div = document.createElement("div");
    $div.innerHTML = `<div
        class="toast"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        data-autohide="true"
        data-delay="3000"
        style="color: #333;"
      >
        <div class="toast-header">
          <strong class="mr-auto">Alerta</strong>
          <small class="text-muted">${new Date()}</small>
          <button
            type="button"
            class="ml-2 mb-1 close"
            data-dismiss="toast"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="toast-body">
          Se ha detectado movimiento
        </div>
      </div>`;
    toastContainer.appendChild($div.firstChild);
    $(document).ready(function () {
      $(".toast").toast("show");
    });
  }
}, 3000);

async function moveCamera(degrees) {
  const url =
    "https://api.particle.io/v1/devices/34002a000f47363336383437/direccion?access_token=a53bb6163a6680eebfcc6c8aec76d011bec713c6";
  const data = {
    params: degrees,
  };
  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}
