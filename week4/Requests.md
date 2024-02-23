# Requests::Request

### 시작하기에 앞서

1. 오픈소스를 볼 떄 제일 먼저 보면 괜찮은 파일 → Test 파일들
2. Depth 가 깊어지더라도, 초기 이해를 높기위한 전개도는 준비할 것 

---

### Request 알아보기

1. 파일위치 : src/requests/api.py

해당 파일에 위치에 존재하는 함수 request에 대해서 알아보기 

```python
def request(method, url, **kwargs):
	    with sessions.Session() as session:
        return session.request(method=method, url=url, **kwargs)
```

- 해당 함수는 session의 request를 반환하게 되어짐

1. 파일위치 : src/requests/session.py

해당 파일에 위치하는 함수 reqeust에 대해서 알아보기

```python
def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):
# Create the Request.
        req = Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
        )
        prep = self.prepare_request(req)

        proxies = proxies or {}

        settings = self.merge_environment_settings(
            prep.url, proxies, stream, verify, cert
        )

        # Send the request.
        send_kwargs = {
            "timeout": timeout,
            "allow_redirects": allow_redirects,
        }
        send_kwargs.update(settings)
        resp = self.send(prep, **send_kwargs)

        return resp
```

- 해당 함수는 네트워크에 사용되는 인자를 받으며, 인자들의 내용은 주석처리가 되어있음
- Request라는 객체를 생성하며, 이러한 동작은 Depth를 증가할때마다 처리하는 역할을 줄여가는 형태를 가짐
- 또한 prep 라는 변수에 prepare_request(req) 함수가 실행이되어짐

1. prepare_request(req)

```python
    def prepare_request(self, request):
        """Constructs a :class:`PreparedRequest <PreparedRequest>` for
        transmission and returns it. The :class:`PreparedRequest` has settings
        merged from the :class:`Request <Request>` instance and those of the
        :class:`Session`.

        :param request: :class:`Request` instance to prepare with this
            session's settings.
        :rtype: requests.PreparedRequest
        """
        cookies = request.cookies or {}

        # Bootstrap CookieJar.
        if not isinstance(cookies, cookielib.CookieJar):
            cookies = cookiejar_from_dict(cookies)

        # Merge with session cookies
        merged_cookies = merge_cookies(
            merge_cookies(RequestsCookieJar(), self.cookies), cookies
        )

        # Set environment's basic authentication if not explicitly set.
        auth = request.auth
        if self.trust_env and not auth and not self.auth:
            auth = get_netrc_auth(request.url)

        p = PreparedRequest()
        p.prepare(
            method=request.method.upper(),
            url=request.url,
            files=request.files,
            data=request.data,
            json=request.json,
            headers=merge_setting(
                request.headers, self.headers, dict_class=CaseInsensitiveDict
            ),
            params=merge_setting(request.params, self.params),
            auth=merge_setting(auth, self.auth),
            cookies=merged_cookies,
            hooks=merge_hooks(request.hooks, self.hooks),
        )
        return p
```

- request 객체를 준비하는 함수로, cookies들의 병합, auth 정보를 정리하고 이를 객체로 생성하여 PreparedRequest객체로 반환을 진행함
- 반환된 객체는 다시 session.py에서 session.request 함수를 통해 send 함수의 인자로 사용되어짐
    - 이는 준비된 요청을 보낸다는 TASK를 수행함

1. session.send()

```python
def send(self, request, **kwargs):
        """Send a given PreparedRequest.

        :rtype: requests.Response
        """
        # Set defaults that the hooks can utilize to ensure they always have
        # the correct parameters to reproduce the previous request.
        kwargs.setdefault("stream", self.stream)
        kwargs.setdefault("verify", self.verify)
        kwargs.setdefault("cert", self.cert)
        if "proxies" not in kwargs:
            kwargs["proxies"] = resolve_proxies(request, self.proxies, self.trust_env)

        # It's possible that users might accidentally send a Request object.
        # Guard against that specific failure case.
        if isinstance(request, Request):
            raise ValueError("You can only send PreparedRequests.")

        # Set up variables needed for resolve_redirects and dispatching of hooks
        allow_redirects = kwargs.pop("allow_redirects", True)
        stream = kwargs.get("stream")
        hooks = request.hooks

        # Get the appropriate adapter to use
        adapter = self.get_adapter(url=request.url)

        # Start time (approximately) of the request
        start = preferred_clock()

        # Send the request
        r = adapter.send(request, **kwargs)

        # Total elapsed time of the request (approximately)
        elapsed = preferred_clock() - start
        r.elapsed = timedelta(seconds=elapsed)

        # Response manipulation hooks
        r = dispatch_hook("response", hooks, r, **kwargs)

        # Persist cookies
        if r.history:
            # If the hooks create history then we want those cookies too
            for resp in r.history:
                extract_cookies_to_jar(self.cookies, resp.request, resp.raw)

        extract_cookies_to_jar(self.cookies, request, r.raw)

        # Resolve redirects if allowed.
        if allow_redirects:
            # Redirect resolving generator.
            gen = self.resolve_redirects(r, request, **kwargs)
            history = [resp for resp in gen]
        else:
            history = []

        # Shuffle things around if there's history.
        if history:
            # Insert the first (original) request at the start
            history.insert(0, r)
            # Get the last request made
            r = history.pop()
            r.history = history

        # If redirects aren't being followed, store the response on the Request for Response.next().
        if not allow_redirects:
            try:
                r._next = next(
                    self.resolve_redirects(r, request, yield_requests=True, **kwargs)
                )
            except StopIteration:
                pass

        if not stream:
            r.content

        return r

```

1. 인자로 전달받은 prepare_request 와 키워드 인자를 통해 , 프록시,리다이렉션,훅,스트림에 대한 정보를 저장
2. 요청 url을 가지는 adapter를 getter를 통해 adpater 객체를 생성하여
3. adpater.send 함수를 사용하여, prepare_request의 객체를 전송함

### [Adapter](http://Adapter.py).HTTPAdapter

1. requests의 네트워크 통신에 대한 내용은 urllib를 사용하여 구현이되어 있음
2. 느슨한 결합성을 사용하여 http 통신과 https 통신이 가능하도록 설계되어 있음