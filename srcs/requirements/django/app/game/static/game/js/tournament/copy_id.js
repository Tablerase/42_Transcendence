document.getElementById('copyText').addEventListener('click', function () {
  const copyID = document.getElementById('copyID');
  const originalText = copyID.innerText;

  const tempInput = document.createElement('input');
  tempInput.value = originalText;
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand('copy');
  document.body.removeChild(tempInput);

  copyID.innerText = 'Copied!';

  setTimeout(() => {
    copyID.innerText = originalText;
  }, 1500);
});
