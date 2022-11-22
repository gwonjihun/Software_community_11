const loginBtn = document.querySelector ('.login');
const loginInfo = document.querySelector ('.loginInfo');

loginBtn.addEventListener ('click', e => {
  e.preventDefault ();
  console.log ('test', e.target.textContent);
  if (e.target.textContent === '로그인') {
    e.target.textContent = '로그아웃';
  } else {
    e.target.textContent = '로그인';
  }
  loginInfo.classList.toggle ('active');
});
