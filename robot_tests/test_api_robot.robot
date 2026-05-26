*** Settings ***
Library    RequestsLibrary
Library    Collections
Suite Setup    Create Session    jsonplaceholder    https://jsonplaceholder.typicode.com

*** Test Cases ***
GET list of posts
    [Documentation]    Pobiera listę postów i sprawdza kod odpowiedzi oraz że odpowiedź jest listą
    ${resp}=    GET On Session    jsonplaceholder    /posts
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Contain    ${resp.headers['Content-Type']}    application/json
    ${body}=    Call Method    ${resp}    json
    Should Be True    isinstance(${body}, list)
    ${count}=    Get Length    ${body}
    Log    Found ${count} posts

GET single post
    [Documentation]    Pobiera post o id=1 i sprawdza pola
    ${resp}=    GET On Session    jsonplaceholder    /posts/1
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Contain    ${resp.headers['Content-Type']}    application/json
    ${post}=    Call Method    ${resp}    json
    Dictionary Should Contain Key    ${post}    id
    Should Be Equal As Integers    ${post['id']}    1
    Dictionary Should Contain Key    ${post}    title

POST create new post
    [Documentation]    Tworzy nowy post (API zwraca symulowany rezultat) i sprawdza status 201
    ${payload}=    Create Dictionary    title=foo    body=bar    userId=1
    ${resp}=    POST On Session    jsonplaceholder    /posts    json=${payload}
    Should Be Equal As Integers    ${resp.status_code}    201
    Should Contain    ${resp.headers['Content-Type']}    application/json
    ${created}=    Call Method    ${resp}    json
    Dictionary Should Contain Key    ${created}    id

PUT update post
    [Documentation]    Aktualizuje post o id=1 i sprawdza, że tytuł został zmieniony
    ${update}=    Create Dictionary    id=1    title=updated    body=bar    userId=1
    ${resp}=    PUT On Session    jsonplaceholder    /posts/1    json=${update}
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Contain    ${resp.headers['Content-Type']}    application/json
    ${updated}=    Call Method    ${resp}    json
    Should Be Equal    ${updated['title']}    updated

DELETE post
    [Documentation]    Usuwa post o id=1 (symulacja) i sprawdza kod odpowiedzi
    ${resp}=    DELETE On Session    jsonplaceholder    /posts/1
    Should Be Equal As Integers    ${resp.status_code}    200
    Should Contain    ${resp.headers['Content-Type']}    application/json
