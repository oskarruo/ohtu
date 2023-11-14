*** Settings ***
Resource  resource.robot
Test Setup  Create User And Input New Command

*** Test Cases ***
Register With Valid Username And Password
    Input Credentials  abc  salasana1
    Output Should Contain  New user registered

Register With Already Taken Username And Valid Password
    Input Credentials  testi  salasana1
    Output Should Contain  User with username testi already exists

Register With Too Short Username And Valid Password
    Input Credentials  ab  salasana1
    Output Should Contain  Username needs to be at least 3 characters long

Register With Enough Long But Invalid Username And Valid Password
    Input Credentials  abc123  salasana1
    Output Should Contain  Username should only contain characters a-z

Register With Valid Username And Too Short Password
    Input Credentials  abc  salasan
    Output Should Contain  Password needs to be at least 8 characters long

Register With Valid Username And Long Enough Password Containing Only Letters
    Input Credentials  abc  salasana
    Output Should Contain  Password can not be only letters

*** Keywords ***
Create User And Input New Command
    Create User   testi  salasana1
    Input New Command
