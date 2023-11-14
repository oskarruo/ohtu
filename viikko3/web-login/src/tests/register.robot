*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  testi
    Set Password  salasana1
    Set Password Confirmation  salasana1
    Submit Credentials
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  te
    Set Password  salasana1
    Set Password Confirmation  salasana1
    Submit Credentials
    Register Should Fail With Message  Username needs to be at least 3 characters long

Register With Valid Username And Invalid Password
    Set Username  test
    Set Password  salasana
    Set Password Confirmation  salasana
    Submit Credentials
    Register Should Fail With Message  Password can not be only letters
    Set Username  test
    Set Password  salasan
    Set Password Confirmation  salasan
    Submit Credentials
    Register Should Fail With Message  Password needs to be at least 8 characters long

Register With Nonmatching Password And Password Confirmation
    Set Username  testing
    Set Password  salasana1
    Set Password Confirmation  salasana12
    Submit Credentials
    Register Should Fail With Message  The passwords are different

Login After Successful Registration
    Set Username  testtest
    Set Password  salasana1
    Set Password Confirmation  salasana1
    Submit Credentials
    Go To Login Page
    Set Username  testtest
    Set Password  salasana1
    Submit Credentials Login
    Login Should Succeed

Login After Failed Registration
    Set Username  testingtest
    Set Password  salasana
    Set Password Confirmation  salasana
    Submit Credentials
    Go To Login Page
    Set Username  testingtest
    Set Password  salasana
    Submit Credentials Login
    Login Should Fail With Message  Invalid username or password

*** Keywords ***
Submit Credentials
    Click Button  Register

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Login Should Succeed
    Main Page Should Be Open

Submit Credentials Login
    Click Button  Login

Login Should Fail With Message
    [Arguments]  ${message}
    Login Page Should Be Open
    Page Should Contain  ${message}