setInterval(async () => {
  const response = await fetch("http://127.0.0.1:5000/api/motion", {
    mode: "cors",
  });
}, 500);
