$("#register-button").click(userRegister);

function userRegister(){
  newUsername = $("#register-username").text();
  newPassword = $("#register-password").text();
  console.log("My username is: " + newUsername + " and my password is: " + newPassword);
}
