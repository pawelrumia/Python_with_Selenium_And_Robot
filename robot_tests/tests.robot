*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Suite Setup    Log    Starting Robot test suite
Suite Teardown    Log    Suite finished

*** Variables ***
${URL}    https://the-internet.herokuapp.com/
${RESULTS_DIR}    results

*** Test Cases ***
Home page - basic smoke
    [Documentation]    Open the home page and verify title, heading and content visibility with waits and extra assertions
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Create Directory    ${RESULTS_DIR}

    # wait for main heading to appear and be visible
    Wait Until Element Is Visible    xpath=//h1    timeout=15s
    Element Should Be Visible    xpath=//h1
    # check header text contains expected words (case-insensitive)
    ${heading}=    Get Text    xpath=//h1
    Should Match Regexp    ${heading}    (?i).*internet.*
    # ensure page title is correct (with a small retry window)
    Wait Until Keyword Succeeds    3 times    3s    Title Should Be    The Internet

    # --- robustly verify content links inside #content ---
    ${links_xpath}=    Set Variable    xpath=//div[@id='content']//a
    Wait Until Page Contains Element    ${links_xpath}    timeout=20s
    # scroll first link into view using JS selector to avoid passing WebElement to JS
    Execute JavaScript    document.querySelector('div#content a').scrollIntoView(true);
    Sleep    0.5s
    ${visible}=    Run Keyword And Return Status    Wait Until Element Is Visible    ${links_xpath}    timeout=10s
    Run Keyword If    '${visible}'=='False'    Capture Page Screenshot    ${RESULTS_DIR}/failure_links_not_visible.png
    Run Keyword If    '${visible}'=='False'    ${src}=    Get Source
    Run Keyword If    '${visible}'=='False'    Create File    ${RESULTS_DIR}/failure_page_source.html    ${src}
    Run Keyword If    '${visible}'=='False'    Fail    Links inside #content are not visible after wait. See ${RESULTS_DIR} for screenshot and page source.

    # verify that a known link 'A/B Testing' exists and is visible
    Element Should Be Visible    xpath=//div[@id='content']//a[normalize-space(.)='A/B Testing']

    # additional sanity checks
    Page Should Contain    A/B Testing
    [Teardown]    Close Browser

Homepage - quick links checks
    [Documentation]    Simple checks: count links and verify some common links are present and visible
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Wait Until Element Is Visible    xpath=//h1    timeout=10s
    ${count}=    Get Element Count    xpath=//div[@id='content']//a
    Log    Found ${count} links inside #content
    Should Be True    ${count} >= 10
    Element Should Be Visible    xpath=//div[@id='content']//a[normalize-space(.)='Form Authentication']
    Element Should Be Visible    xpath=//div[@id='content']//a[normalize-space(.)='Dropdown']
    [Teardown]    Close Browser

A/B Testing page opens
    [Documentation]    Click A/B Testing link and verify page heading and content
    Open Browser    ${URL}    chrome
    Maximize Browser Window
    Wait Until Element Is Visible    xpath=//h1    timeout=10s
    Click Element    xpath=//div[@id='content']//a[normalize-space(.)='A/B Testing']
    Wait Until Element Is Visible    xpath=//h3    timeout=10s
    ${ab_heading}=    Get Text    xpath=//h3
    # accept headings like 'A/B Test Control' or other variants containing 'A/B'
    Should Match Regexp    ${ab_heading}    (?i).*a/b.*
    # check that example paragraph exists
    Element Should Be Visible    css=div.example p
    [Teardown]    Close Browser
