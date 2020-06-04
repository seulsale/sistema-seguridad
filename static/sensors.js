$(".toast").toast("show");

setInterval(async () => {
  let req = await fetch("http://127.0.0.1:5000/api/motion", {
    mode: "cors",
  });
  let res = await req.json();
  console.log(res.movement);
}, 1000);

async function moveCamera(degrees) {
  const url =
    "https://api.particle.io/v1/devices/34002a000f47363336383437/feed?access_token=a53bb6163a6680eebfcc6c8aec76d011bec713c6";
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
