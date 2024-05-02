# HTTPConnectionPool

### 해당 클래스는 이중상속중입니다.

```python
class HTTPConnectionPool(ConnectionPool, RequestMethods):
```

- ConnectionPool : 클래스의 연결 관리, 생애주기 관리, 필요한 연결을 관리하는 클래스
    - 스레드-세이프 기능을 지원
        - 멀티스레드 환경에서 여러 스레드가 동시에 같은 코드 블록, 데이터 구조, 파일, 메모리 등을 안전하게 접근하거나 수정할 수 있도록 설계된 기능을 말합니다
        - 데이터 일관성, 동시성 오류 방지, 프로그램 안정성과 신뢰성 향상
        - 구현 방법 → 알 공부
            - 락 및 뮤텍스
            - 세마포어
            - 원자적 연산
            - 스레드 로컬 스토리지 : 스레드 자신만의 데이터 사본을 갖도록 하여 공유 자원
        
    - 연결의 최대 사이즈 관리 가능
    - 필요에 따른 연결을 재사용 또는 생성
    - 연결이 사용가능할 때 까지 요청을 차단하거나 연결 요청 거부
- RequestMethods: HTTP 요청에 필요한 메서드를 제공
    - GET,POST,PUT,DELETE
    - URL과 헤더 바디등의 데이터를 사용하여, HTTP 요청을 구성하고 전송
    - 요청을 보낼때 사용자가 제공한 헤더나 데이터를 요청메세지 포함
    - 응답을 처리하고 결과를 반환

---

### 개발자가 남긴 주석

1. **host**:
    - 이 매개변수는 HTTP 연결에 사용될 호스트 이름을 지정합니다. 예를 들어 "localhost"와 같이 지정할 수 있습니다. 이 값은 **`http.client.HTTPConnection`** 클래스로 전달됩니다.
2. **port**:
    - 이 매개변수는 호스트에 연결할 때 사용할 포트 번호를 지정합니다. 기본값은 **`None`**이며, 이 경우 표준 HTTP 포트인 80이 사용됩니다.
3. **timeout**:
    - 각 연결에 대한 소켓 타임아웃을 초 단위로 설정합니다. 이 값은 단순한 숫자(정수 또는 부동 소수점)일 수도 있고, 더 세밀한 제어를 위해 **`urllib3.util.Timeout`** 인스턴스일 수도 있습니다. 객체 생성 후, 이 값은 항상 **`urllib3.util.Timeout`** 객체로 설정됩니다.
4. **maxsize**:
    - 재사용 가능한 연결의 최대 수를 지정합니다. 이 값이 1보다 크면 멀티스레드 상황에서 유용하며, **`block`**이 **`False`**로 설정된 경우 더 많은 연결이 생성되지만 사용 후에는 저장되지 않습니다.
5. **block**:
    - **`True`**로 설정되면, **`maxsize`** 이상의 연결은 동시에 사용되지 않습니다. 사용 가능한 연결이 없을 때는 연결이 해제될 때까지 호출이 차단됩니다. 이는 특정 멀티스레드 환경에서 호스트당 최대 연결 수를 제한하여 서버에 부하를 주지 않기 위해 유용합니다.
6. **headers**:
    - 모든 요청에 기본적으로 포함될 HTTP 헤더입니다. 명시적으로 다른 헤더가 제공되지 않는 한 이 헤더들이 사용됩니다.
7. **retries**:
    - 이 풀을 사용하는 요청에 기본적으로 적용될 재시도(retry) 설정입니다. 네트워크 오류나 일시적인 문제가 발생했을 때 요청을 자동으로 다시 시도하는 방법을 구성할 수 있습니다.
8. **_proxy**:
    - 파싱된 프록시 URL입니다. 이 매개변수는 직접 사용되어서는 안 되며, 대신 **`urllib3.ProxyManager`**를 사용해야 합니다.
9. **_proxy_headers**:
    - 프록시를 사용할 때 적용될 헤더의 사전입니다. 이것도 직접 사용되어서는 안 되며, **`urllib3.ProxyManager`**를 통해 사용해야 합니다.
10. *\**conn_kw**:
    - 새로운 **`urllib3.connection.HTTPConnection`** 또는 **`urllib3.connection.HTTPSConnection`** 인스턴스를 생성할 때 사용될 추가 매개변수들입니다.
    

---

### 그날.. 우리가 막힌 날..

```python
scheme = "http"
ConnectionCls: (
        type[BaseHTTPConnection] | type[BaseHTTPSConnection]
    ) = HTTPConnection
```

1. scheme : 사용할 프로토콜
2. ConnectionCls : BaseHTTPConnection 또는 BaseHTTPSConnection 의 타입힌트를 가지면 HTTPConnection으로 할당을 진행합니다.
    
    → **HTTP 또는 HTTPS 의 베이스 커낵션이 오면 HTTPConnection으로 할당을 진행하는 코드**
    

---

### 초기화… 해야겠지?

![인자의 타입힌트](HTTPConnectionPool%205d46dc297d3e406c9d4417ca05b52b83/Untitled.png)

인자의 타입힌트

```python
ConnectionPool.__init__(self, host, port)
RequestMethods.__init__(self, headers)

```

상위 클래스에 대하여 초기화를 진행합니다.

```python
if not isinstance(timeout, Timeout):
  timeout = Timeout.from_float(timeout)
```

timeoutdl Timeout 객체가 아닌 경우 변환을 진행하여 timeout에 적용

```python

        if retries is None:
            retries = Retry.DEFAULT
```

retries 가 없을 경우 Retry는 기본 설정값을 자식값으로 가진다

```python
        self.timeout = timeout
        self.retries = retries
```

---

```python
        self.pool: queue.LifoQueue[typing.Any] | None = self.QueueCls(maxsize)
        self.block = block

        self.proxy = _proxy
        self.proxy_headers = _proxy_headers or {}
        self.proxy_config = _proxy_config
```

LIFO 큐를 사용하여, 큐의 관리를 진행함

1. 연결 재사용 최적화 : Time locality, 핸드 쉐이크를 소요하는 시간과 리소스 절약 가능
2. 연결 상태 유지 : persistent-http를 사용할 확률이 높아진다 
3. 리소스 활용 극대화 : persistent-http 사용할 확률이 높아진다
4. 성능 향상 : 열린 연결을 계속하세 사용하여, 성능 향상
5. 타임아웃 관리 : Connection-Freshness

### **헤더와 `or {}`의 사용 예**

이러한 사용법은 특히 네트워킹, API 호출, 또는 어떤 설정을 요구하는 함수에서 매개변수가 제공되지 않았을 때 기본 값을 제공하는 방식으로 사용됩니다. 예를 들어, 프록시 설정이나 HTTP 요청에서 헤더를 다룰 때, 헤더가 **`None`**인 경우 빈 딕셔너리 **`{}`**로 초기화하여 후속 코드에서 키-값 쌍을 추가하거나 조회할 때 오류가 발생하지 않도록 합니다.

---

**`maxsize`**만큼의 **`None`** 요소를 가진 큐를 생성하여 초기화합니다. 이 큐는 **`self.pool`**에 저장됩니다. 큐의 최대 크기는 **`maxsize`**로 지정

```python
        for _ in range(maxsize):
            self.pool.put(None
```

테스트 및 디버깅을 위한 몇 가지 변수를 초기화. **`self.num_connections`** 및 **`self.num_requests`**는 연결 및 요청의 수를 추적용 변수. **`self.conn_kw`**는 연결 구성에 대한 추가 옵션을 저장하는 딕셔너리입니다. 즉, 해당 클래스에 한 멤버변수를 할당하는 작업입니다.

```python
        # These are mostly for testing and debugging purposes.
        self.num_connections = 0
        self.num_requests = 0
        self.conn_kw = conn_kw
```

만약 **`self.proxy`**가 설정, 프록시를 사용 진행 [Nagle의 알고리즘](https://www.notion.so/Naggle-s-Algorithmn-97b904898fc440dd910fb55f83df6822?pvs=21)을 사용하여 패킷 단편화를 피하기 위해 소켓 옵션을 설정. 소켓 옵션은 **`self.conn_kw`** 딕셔너리의 **`"socket_options"`** 키에 추가됩니다.

```python
        if self.proxy:
            # Enable Nagle's algorithm for proxies, to avoid packet fragmentation.
            # We cannot know if the user has added default socket options, so we cannot replace the
            # list.
            self.conn_kw.setdefault("socket_options", [])

            self.conn_kw["proxy"] = self.proxy
            self.conn_kw["proxy_config"] = self.proxy_config
```

[Naggle’s Algorithmn](https://www.notion.so/Naggle-s-Algorithmn-97b904898fc440dd910fb55f83df6822?pvs=21)

**`weakref.finalize`** 함수를 사용하여 객체가 파괴될 때 호출될 콜백 함수를 등록합니다. 

이 경우 **`_close_pool_connections`** 함수가 등록 진행. 이 함수는 HTTPConnectionPool에서 연결을 닫습니다. **`finalize`** 함수에는 파괴될 객체와 해당 객체를 파괴할 때 호출될 함수가 전달됩니다. 이때 **`self`**를 직접 넘기지 않고, **`self.pool`**을 넘기는 이유는, **`finalize`**가 객체에 대한 참조를 유지하지 않고도 객체가 파괴될 때 연결 풀을 닫을 수 있도록 하기 위해서입니다. 

- 약한 참조와 강한 참조
    - **강한 참조(Strong Reference)**: 파이썬에서 객체에 대한 기본적인 참조 방식입니다. 객체에 대한 강한 참조가 존재하는 한, 그 객체는 메모리에 유지됩니다. 즉, 객체의 참조 카운트가 0이 되지 않는 한 객체는 가비지 컬렉션의 대상이 되지 않습니다.
    - **약한 참조(Weak Reference)**: 객체를 참조하지만, 참조 카운트를 증가시키지 않습니다. 약한 참조는 객체가 다른 곳에서 이미 사용되지 않을 때 자유롭게 메모리에서 해제될 수 있도록 합니다. 즉, 약한 참조만이 객체를 가리키고 있을 경우, 그 객체는 가비지 컬렉션에 의해 수집될 수 있습니다.
- Finalize 와 약한참조의 관계
    
    **`finalize`**가 객체에 강한 참조를 사용한다면, **`finalize`** 자체가 객체의 참조 카운트를 증가시켜 객체가 필요하지 않음에도 불구하고 메모리에서 해제되지 않는 상황이 발생할 수 있음
    

```python
        # Do not pass 'self' as callback to 'finalize'.
        # Then the 'finalize' would keep an endless living (leak) to self.
        # By just passing a reference to the pool allows the garbage collector
        # to free self if nobody else has a reference to it.
        pool = self.pool

        # Close all the HTTPConnections in the pool before the
        # HTTPConnectionPool object is garbage collected.
        weakref.finalize(self, _close_pool_connections, pool)
```

---

```python
    def _new_conn(self) -> BaseHTTPConnection:
        """
        Return a fresh :class:`HTTPConnection`.
        """
        self.num_connections += 1
        log.debug(
            "Starting new HTTP connection (%d): %s:%s",
            self.num_connections,
            self.host,
            self.port or "80",
        )

        conn = self.ConnectionCls(
            host=self.host,
            port=self.port,
            timeout=self.timeout.connect_timeout,
            **self.conn_kw,
        )
        return conn
```

새로운 HTTP 연결을 생성하는 역할을 합니다. 코드를 해석해보겠습니다.

1. **`self.num_connections`** 값을 1 증가시킵니다. 현재까지 생성된 HTTP 연결의 수를 추적
    
    ```python
            self.num_connections += 1
    ```
    
2. 디버그 로그를 생성. 새로운 HTTP 연결이 시작될 때 출력
    
    ```python
            log.debug(
                "Starting new HTTP connection (%d): %s:%s",
                self.num_connections,
                self.host,
                self.port or "80",
            )
    ```
    
3. **`self.ConnectionCls`**를 사용하여 새로운 HTTP 연결 객체를 생성 **`self.ConnectionCls`**는 클래스의 속성으로 설정되며,생성된 연결에는 호스트, 포트 및 연결 시간 제한에 대한 정보가 전달됩니다. 추가적인 연결 설정은 **`self.conn_kw`**에 저장된 딕셔너리에서 가져옵니다.
    
    ```python
            conn = self.ConnectionCls(
                host=self.host,
                port=self.port,
                timeout=self.timeout.connect_timeout,
                **self.conn_kw,
            )
    ```
    
4. 새로운 연결 객체를 반환

---

### “_get_conn”

HTTP 연결 풀에서 연결 객체를 반환하는 역할을 수행하는 함수. 함수는 여러 가능성을 고려하여 구현되어 있으며, 특정 조건에서는 새로운 연결을 생성하거나 오류를 생성함

```python
    def _get_conn(self, timeout: float | None = None) -> BaseHTTPConnection:
        """
        Get a connection. Will return a pooled connection if one is available.

        If no connections are available and :prop:`.block` is ``False``, then a
        fresh connection is returned.

        :param timeout:
            Seconds to wait before giving up and raising
            :class:`urllib3.exceptions.EmptyPoolError` if the pool is empty and
            :prop:`.block` is ``True``.
        """
        conn = None

        if self.pool is None:
            raise ClosedPoolError(self, "Pool is closed.")

        try:
            conn = self.pool.get(block=self.block, timeout=timeout)

        except AttributeError:  # self.pool is None
            raise ClosedPoolError(self, "Pool is closed.") from None  # Defensive:

        except queue.Empty:
            if self.block:
                raise EmptyPoolError(
                    self,
                    "Pool is empty and a new connection can't be opened due to blocking mode.",
                ) from None
            pass  # Oh well, we'll create a new connection then

        # If this is a persistent connection, check if it got disconnected
        if conn and is_connection_dropped(conn):
            log.debug("Resetting dropped connection: %s", self.host)
            conn.close()

        return conn or self._new_conn()
```

1. **함수 정의 및 매개변수**:
    - **`_get_conn(self, timeout: float | None = None) -> BaseHTTPConnection`**:
    이 함수는 선택적 **`timeout`** 매개변수를 받아들이며, 이는 연결을 기다리는 최대 시간(초)을 설정합니다. **`timeout`**이 **`None`**일 경우, 기본 설정된 시간이 사용됩니다.
2. **연결 풀 검증**:
    - 함수는 먼저 **`self.pool`**이 **`None`**인지 확인하여, 연결 풀이 이미 닫혀있는지를 검사합니다. 만약 연결 풀이 닫혀 있으면, **`ClosedPoolError`** 예외를 발생
3. **연결 객체 얻기**:
    - **`self.pool.get(block=self.block, timeout=timeout)`**:
    이 호출은 연결 풀에서 연결 객체를 얻습니다. **`block`** 매개변수는 풀이 비어있을 때 함수가 차단 모드로 동작할지 결정하며, **`timeout`**은 연결을 얻기 위해 기다릴 최대 시간을 설정합니다.
4. **예외 처리**:
    - **`AttributeError`**: **`self.pool`**이 **`None`**이 되어 속성이 없는 경우 다시 **`ClosedPoolError`**를 발생시킵니다.
        
        ```python
        except AttributeError:  # self.pool is None
                    raise ClosedPoolError(self, "Pool is closed.") from None
        ```
        
    - **`queue.Empty`**: 연결 풀이 비어있고, **`block`**이 **`True`**로 설정되어 새 연결을 생성할 수 없을 경우 **`EmptyPoolError`**를 발생시킵니다. **`block`**이 **`False`**일 경우, 새 연결 생성을 위해 다음 단계로 넘어갑니다.
        
        ```python
        except queue.Empty:
                    if self.block:
                        raise EmptyPoolError(
                            self,
                            "Pool is empty and a new connection can't be opened due to blocking mode.",
                        ) from None
                    pass
        ```
        
5. **연결 상태 검사**:
    - 만약 연결이 반환되었지만, 연결이 끊긴 상태라면(**`is_connection_dropped(conn)`**), 해당 연결을 닫고 로그를 남깁니다.
    
    ```python
    if conn and is_connection_dropped(conn):
                log.debug("Resetting dropped connection: %s", self.host)
                conn.close()
    ```
    
6. **연결 반환**:
    - **`conn or self._new_conn()`**:
    만약 유효한 연결 객체(**`conn`**)가 있으면 그대로 반환하고, 그렇지 않으면 **`_new_conn()`** 메서드를 호출하여 새 연결 객체를 생성하고 반환합니다.

---

### “_put_conn”

HTTP 연결 객체를 연결 풀에 반환하는 역할을 수행합니다. 이 함수는 연결 풀의 상태에 따라 연결을 풀에 다시 추가하거나, 필요한 경우 연결을 종료하고 버립니다.

```python
    def _put_conn(self, conn: BaseHTTPConnection | None) -> None:
        """
        Put a connection back into the pool.

        :param conn:
            Connection object for the current host and port as returned by
            :meth:`._new_conn` or :meth:`._get_conn`.

        If the pool is already full, the connection is closed and discarded
        because we exceeded maxsize. If connections are discarded frequently,
        then maxsize should be increased.

        If the pool is closed, then the connection will be closed and discarded.
        """
        if self.pool is not None:
            try:
                self.pool.put(conn, block=False)
                return  # Everything is dandy, done.
            except AttributeError:
                # self.pool is None.
                pass
            except queue.Full:
                # Connection never got put back into the pool, close it.
                if conn:
                    conn.close()

                if self.block:
                    # This should never happen if you got the conn from self._get_conn
                    raise FullPoolError(
                        self,
                        "Pool reached maximum size and no more connections are allowed.",
                    ) from None

                log.warning(
                    "Connection pool is full, discarding connection: %s. Connection pool size: %s",
                    self.host,
                    self.pool.qsize(),
                )

        # Connection never got put back into the pool, close it.
        if conn:
            conn.close()
```

1. **함수 정의 및 매개변수**:
    - **`_put_conn(self, conn: BaseHTTPConnection | None) -> None`**:
    이 함수는 **`BaseHTTPConnection`** 타입 또는 **`None`**의 **`conn`** 매개변수를 받습니다. 이 매개변수는 연결 객체를 나타냅니다.
2. **연결 풀 검증**:
    - 함수는 먼저 **`self.pool`**이 **`None`**이 아닌지 확인합니다. **`None`**이면 더 이상의 작업을 수행하지 않고 함수가 종료됩니다.
        
        ```python
        if self.pool is not None:
        ```
        
3. **연결 객체 반환 시도**:
    - **`self.pool.put(conn, block=False)`**:
    이 호출은 연결 객체를 연결 풀에 반환하려고 시도합니다. **`block=False`**는 연결 풀이 가득 차 있을 경우, 즉시 예외를 발생시키지 않고 반환을 시도합니다.
        
        ```python
        try:
        	self.pool.put(conn, block=False)
        	return
        ```
        
4. **예외 처리**:
    - **`AttributeError`**: **`self.pool`**이 **`None`**인 경우 처리합니다. 여기서는 특별한 동작 없이 넘어갑니다.
        
        ```python
        except AttributeError:
                        # self.pool is None.
                        pass
        ```
        
    - **`queue.Full`**: 연결 풀이 가득 차 있어 연결 객체를 풀에 추가할 수 없을 경우, 해당 연결을 종료합니다. 이 상황에서 **`self.block`**이 **`True`**라면, 함수는 연결이 반환될 수 없다는 **`FullPoolError`**를 발생시킵니다.
        
        ```python
                        if self.block:
                            # This should never happen if you got the conn from self._get_conn
                            raise FullPoolError(
                                self,
                                "Pool reached maximum size and no more connections are allowed.",
                            ) from None
        
        ```
        
5. **경고 로그**:
    - 연결 풀이 가득 찼을 때, 연결이 폐기되는 상황을 경고하는 로그 메시지를 출력합니다. 이는 풀 관리에 있어 **`maxsize`**를 조정할 필요가 있음을 알릴 때 유용합니다.
    
    ```python
                    log.warning(
                        "Connection pool is full, discarding connection: %s. Connection pool size: %s",
                        self.host,
                        self.pool.qsize(),
                    )
    ```
    
6. **연결 종료**:
    - **`if conn:`** 절을 통해, 만약 **`conn`**이 유효하면 해당 연결을 닫습니다. 이는 연결 풀이 닫혀 있거나, 연결 풀에 추가할 수 없을 때 수행됩니다.
    
    상황 
    
    - 연결 풀이 가득 찼을 경우
    - 연결 풀이 닫혀 있는 경우
    
    ```python
            # Connection never got put back into the pool, close it.
            if conn:
                conn.close()
    ```
    

---

### 유틸 함수

1. **`_validate_conn` 함수**:
    - 이 함수는 요청을 보내기 직전, 소켓이 생성된 후에 호출됩니다. 함수의 내용이 비어 있어서 현재는 아무런 검증이나 추가 작업을 수행하지 않지만, 필요한 검증 로직을 추가할 수 있는 장소로 활용될 수 있습니다.
    
    ```python
        def _validate_conn(self, conn: BaseHTTPConnection) -> None:
            """
            Called right before a request is made, after the socket is created.
            """
    ```
    
2. **`_prepare_proxy` 함수**:
    - 주석에 따르면, 이 함수는 HTTP 연결에 대해 할 일이 없다고 명시. 프록시 설정이 필요한 HTTPS 연결 등에서 사용될 수 있는 함수의 틀을 제공합니다. 현재는 **`pass`** 키워드를 사용하여 아무런 작업도 수행하지 않습니다.
    
    ```python
        def _prepare_proxy(self, conn: BaseHTTPConnection) -> None:
            # Nothing to do for HTTP connections.
            pass
    ```
    
3. **`_get_timeout` 함수**:
    - 이 함수는 입력받은 **`timeout`** 매개변수를 **`urllib3.util.Timeout`** 클래스의 인스턴스로 변환하는 역할을 합니다. 이를 통해 일관된 타임아웃 처리가 가능합니다.
    - 매개변수 **`timeout`**이 **`_DEFAULT_TIMEOUT`**인 경우, 클래스 인스턴스의 **`clone`** 메서드를 호출하여 기본 타임아웃 설정을 복제합니다.
    - **`timeout`**이 **`Timeout`** 클래스의 인스턴스인 경우, 이 인스턴스의 **`clone`** 메서드를 호출하여 해당 인스턴스를 복제합니다.
    - 그 외의 경우(정수 또는 부동소수점 수로 추정), **`Timeout.from_float(timeout)`**을 호출하여 타임아웃 값을 **`Timeout`** 객체로 변환합니다. 이는 이전 버전과의 호환성을 위해 유지되며, 향후 제거될 수 있습니다.
    
    ```python
        def _get_timeout(self, timeout: _TYPE_TIMEOUT) -> Timeout:
            """Helper that always returns a :class:`urllib3.util.Timeout`"""
            if timeout is _DEFAULT_TIMEOUT:
                return self.timeout.clone()
    
            if isinstance(timeout, Timeout):
                return timeout.clone()
            else:
                # User passed us an int/float. This is for backwards compatibility,
                # can be removed later
                return Timeout.from_float(timeout)
    ```
    

---

### “_raise_timeout”

```python
   def _raise_timeout(
        self,
        err: BaseSSLError | OSError | SocketTimeout,
        url: str,
        timeout_value: _TYPE_TIMEOUT | None,
    ) -> None:
        """Is the error actually a timeout? Will raise a ReadTimeout or pass"""

        if isinstance(err, SocketTimeout):
            raise ReadTimeoutError(
                self, url, f"Read timed out. (read timeout={timeout_value})"
            ) from err

        # See the above comment about EAGAIN in Python 3.
        if hasattr(err, "errno") and err.errno in _blocking_errnos:
            raise ReadTimeoutError(
                self, url, f"Read timed out. (read timeout={timeout_value})"
            ) from err
```

이 Python 함수 **`_raise_timeout`**은 네트워크 요청 중 발생할 수 있는 타임아웃 관련 에러를 처리하는 역할을 수행합니다. 함수는 발생한 에러(**`err`**), 요청된 URL(**`url`**), 그리고 설정된 타임아웃 값(**`timeout_value`**)을 매개변수로 받아들입니다. 이 함수는 특정 타임아웃 에러가 실제로 발생했는지를 판단하고, 조건에 따라 적절한 타임아웃 에러를 발생시킵니다. 아래는 함수의 주요 기능에 대한 설명입니다:

1. **에러 타입 확인**:
    - **`if isinstance(err, SocketTimeout):`**
    이 조건문은 입력받은 에러 객체가 **`SocketTimeout`** 클래스의 인스턴스인지 확인합니다. **`SocketTimeout`**은 소켓 타임아웃을 나타내는 에러 타입입니다. 이 조건이 참일 경우, **`ReadTimeoutError`** 예외를 발생시킵니다.
        
        ```python
                if isinstance(err, SocketTimeout):
                    raise ReadTimeoutError(
                        self, url, f"Read timed out. (read timeout={timeout_value})"
                    ) from err
        ```
        
2. **타임아웃 에러 발생**:
    - **`raise ReadTimeoutError(self, url, f"Read timed out. (read timeout={timeout_value})") from errReadTimeoutError`**는 타임아웃이 발생했을 때 사용하는 사용자 정의 예외입니다. 이 예외를 발생시킬 때, 현재 객체(**`self`**), 문제가 발생한 URL(**`url`**), 그리고 타임아웃 값(**`timeout_value`**)을 포함한 메시지를 전달합니다. **`from err`** 구문은 원래 발생한 에러(**`err`**)와 연관된 새로운 예외를 연결하여 예외 추적에 도움을 줍니다.
    
    ```python
            if isinstance(err, SocketTimeout):
                raise ReadTimeoutError(
                    self, url, f"Read timed out. (read timeout={timeout_value})"
                ) from err
    ```
    
3. **특정 errno를 확인하는 추가 조건**:
    - **`if hasattr(err, "errno") and err.errno in _blocking_errnos:`**
    이 조건문은 에러 객체에 **`errno`** 속성이 있는지, 그리고 그 **`errno`** 값이 **`_blocking_errnos`** 집합에 포함되어 있는지 확인합니다. **`_blocking_errnos`**는 네트워크 작업에서 블로킹 관련 에러 코드들을 나타낼 것입니다. 이 조건이 참일 경우에도 **`ReadTimeoutError`**를 발생시키며, 이는 블로킹 작업에서 발생한 타임아웃을 처리하기 위함입니다.
    
    ```python
            # See the above comment about EAGAIN in Python 3.
            if hasattr(err, "errno") and err.errno in _blocking_errnos:
                raise ReadTimeoutError(
                    self, url, f"Read timed out. (read timeout={timeout_value})"
                ) from err
    ```
    

---

### “_make_request”

```python
    def _make_request(
        self,
        conn: BaseHTTPConnection,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        headers: typing.Mapping[str, str] | None = None,
        retries: Retry | None = None,
        timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
        chunked: bool = False,
        response_conn: BaseHTTPConnection | None = None,
        preload_content: bool = True,
        decode_content: bool = True,
        enforce_content_length: bool = True,
    ) -> BaseHTTPResponse:
```

1. **conn**:
    - **`a connection from one of our connection pools`**
    - 연결 풀에서 가져온 연결 객체입니다. 이 연결을 사용하여 HTTP 요청을 수행합니다.
2. **method**:
    - **`HTTP request method (such as GET, POST, PUT, etc.)`**
    - 수행할 HTTP 요청의 메서드를 지정합니다. 예를 들어 GET, POST, PUT 등이 있습니다.
3. **url**:
    - **`The URL to perform the request on.`**
    - 요청을 보낼 URL입니다.
4. **body**:
    - **`Data to send in the request body, either :class:`**str**`, :class:`**bytes**`, an iterable of :class:`**str**`/:class:`**bytes**`, or a file-like object.`**
    - 요청 본문에 전송할 데이터입니다. 문자열, 바이트, 반복 가능한 문자열/바이트 시퀀스 또는 파일과 같은 객체를 사용할 수 있습니다.
5. **headers**:
    - **`Dictionary of custom headers to send, such as User-Agent, If-None-Match, etc.`**
    - 요청과 함께 보낼 사용자 정의 헤더들의 딕셔너리입니다. 헤더가 지정되지 않으면 연결 풀의 헤더가 사용됩니다.
6. **retries**:
    - **`Configure the number of retries to allow before raising a :class:`**~urllib3.exceptions.MaxRetryError **`exception.`**
    - 요청 실패 시 재시도할 횟수를 설정합니다. **`None`**은 응답을 받을 때까지 무한히 재시도하며, 정수값은 연결 오류에 대해서만 그 횟수만큼 재시도합니다. **`False`**는 재시도를 비활성화합니다.
7. **timeout**:
    - **`If specified, overrides the default timeout for this one request.`**
    - 요청에 대한 타임아웃을 설정합니다. 이 값은 초 단위의 부동소수점 수 또는 **`urllib3.util.Timeout`** 인스턴스일 수 있습니다.
8. **chunked**:
    - **`If True, urllib3 will send the body using chunked transfer encoding.`**
    - **`True`**로 설정하면 청크 전송 인코딩을 사용하여 본문을 전송합니다. 기본값은 **`False`**입니다. `**True**`시 청킹이 가능함
9. **response_conn**:
    - **`Set this to ``None`` if you will handle releasing the connection or set the connection to have the response release it.`**
    - 응답 후 연결을 해제할 책임을 직접 관리하거나 응답이 연결을 해제하도록 설정합니다.
    - 응답을 처리한 후에도 HTTP 연결을 열린 상태로 유지하고자 할 때 사용됩니다. 이 경우 응답을 처리하는 객체가 연결을 관리하고, 필요에 따라 연결을 재사용하거나 추가적인 데이터 전송에 사용할 수 있습니다. → persistant
    - **`response_conn`**이 **`None`**인 경우, **`_make_request`** 함수는 응답 처리 후 연결을 자동으로 닫을 수 있습니다. 이는 주로 **`release_conn`** 매개변수가 **`True`**일 때 발생하며, 연결을 닫고 연결 풀로 반환하게 됩니다. 이 방식은 연결을 적절히 관리하여 자원을 효율적으로 사용하고자 할 때 유용합니다.
        
        ```python
        # 예를 들어, 연결을 유지하고 싶은 경우
        response = _make_request(conn, method, url, response_conn=conn)
        
        # 연결을 자동으로 닫고 싶은 경우
        response = _make_request(conn, method, url, response_conn=None)
        ```
        
10. **preload_content**:
    - **`If True, the response's body will be preloaded during construction.`**
    - **`True`**로 설정하면 응답 본문을 생성 중에 미리 로드합니다.
11. **decode_content**:
    - **`If True, will attempt to decode the body based on the 'content-encoding' header.`**
    - **`True`**로 설정하면 **`content-encoding`** 헤더에 따라 응답 본문을 디코드합니다.
12. **enforce_content_length**:
    - **`Enforce content length checking. Body returned by server must match value of Content-Length header, if present. Otherwise, raise error.`**
    - 응답 본문의 길이가 **`Content-Length`** 헤더와 일치하는지 검증합니다. 일치하지 않을 경우 에러를 발생시킵니다.

---

### make_request 본문

```python
self.num_requests += 1

        timeout_obj = self._get_timeout(timeout)
        timeout_obj.start_connect()
        conn.timeout = Timeout.resolve_default_timeout(timeout_obj.connect_timeout)

        try:
            # Trigger any extra validation we need to do.
            try:
                self._validate_conn(conn)
            except (SocketTimeout, BaseSSLError) as e:
                self._raise_timeout(err=e, url=url, timeout_value=conn.timeout)
                raise

        # _validate_conn() starts the connection to an HTTPS proxy
        # so we need to wrap errors with 'ProxyError' here too.
        except (
            OSError,
            NewConnectionError,
            TimeoutError,
            BaseSSLError,
            CertificateError,
            SSLError,
        ) as e:
            new_e: Exception = e
            if isinstance(e, (BaseSSLError, CertificateError)):
                new_e = SSLError(e)
            # If the connection didn't successfully connect to it's proxy
            # then there
            if isinstance(
                new_e, (OSError, NewConnectionError, TimeoutError, SSLError)
            ) and (conn and conn.proxy and not conn.has_connected_to_proxy):
                new_e = _wrap_proxy_error(new_e, conn.proxy.scheme)
            raise new_e

        # conn.request() calls http.client.*.request, not the method in
        # urllib3.request. It also calls makefile (recv) on the socket.
        try:
            conn.request(
                method,
                url,
                body=body,
                headers=headers,
                chunked=chunked,
                preload_content=preload_content,
                decode_content=decode_content,
                enforce_content_length=enforce_content_length,
            )

        # We are swallowing BrokenPipeError (errno.EPIPE) since the server is
        # legitimately able to close the connection after sending a valid response.
        # With this behaviour, the received response is still readable.
        except BrokenPipeError:
            pass
        except OSError as e:
            # MacOS/Linux
            # EPROTOTYPE and ECONNRESET are needed on macOS
            # https://erickt.github.io/blog/2014/11/19/adventures-in-debugging-a-potential-osx-kernel-bug/
            # Condition changed later to emit ECONNRESET instead of only EPROTOTYPE.
            if e.errno != errno.EPROTOTYPE and e.errno != errno.ECONNRESET:
                raise

        # Reset the timeout for the recv() on the socket
        read_timeout = timeout_obj.read_timeout

        if not conn.is_closed:
            # In Python 3 socket.py will catch EAGAIN and return None when you
            # try and read into the file pointer created by http.client, which
            # instead raises a BadStatusLine exception. Instead of catching
            # the exception and assuming all BadStatusLine exceptions are read
            # timeouts, check for a zero timeout before making the request.
            if read_timeout == 0:
                raise ReadTimeoutError(
                    self, url, f"Read timed out. (read timeout={read_timeout})"
                )
            conn.timeout = read_timeout

        # Receive the response from the server
        try:
            response = conn.getresponse()
        except (BaseSSLError, OSError) as e:
            self._raise_timeout(err=e, url=url, timeout_value=read_timeout)
            raise

        # Set properties that are used by the pooling layer.
        response.retries = retries
        response._connection = response_conn  # type: ignore[attr-defined]
        response._pool = self  # type: ignore[attr-defined]

        # emscripten connection doesn't have _http_vsn_str
        http_version = getattr(conn, "_http_vsn_str", "HTTP/?")
        log.debug(
            '%s://%s:%s "%s %s %s" %s %s',
            self.scheme,
            self.host,
            self.port,
            method,
            url,
            # HTTP version
            http_version,
            response.status,
            response.length_remaining,
        )

        return response
```

1. **요청 준비**:
    - **`self.num_requests += 1`**: 요청 횟수를 하나 증가시킵니다.
    - **`timeout_obj = self._get_timeout(timeout)`**: 사용자가 지정한 타임아웃 값을 가져와 타임아웃 객체를 생성합니다.
    - **`timeout_obj.start_connect()`**: 타임아웃 모니터링을 시작합니다.
    - **`conn.timeout = Timeout.resolve_default_timeout(timeout_obj.connect_timeout)`**: 연결의 타임아웃을 설정합니다.
    
    ```python
    self.num_requests += 1
    
            timeout_obj = self._get_timeout(timeout)
            timeout_obj.start_connect()
            conn.timeout = Timeout.resolve_default_timeout(timeout_obj.connect_timeout)
    ```
    
2. **연결 검증**:
    - **`self._validate_conn(conn)`**: 연결 객체를 검증합니다. 연결이 HTTPS 프록시를 사용한다면, 연결을 시작하는 코드가 이 메소드 내에 포함될 수 있습니다.
    - **`self._raise_timeout(err=e, url=url, timeout_value=conn.timeout)`**: 타임아웃이 발생했을 경우 예외를 발생시킵니다.
    
    ```python
            try:
                # Trigger any extra validation we need to do.
                try:
                    self._validate_conn(conn)
                except (SocketTimeout, BaseSSLError) as e:
                    self._raise_timeout(err=e, url=url, timeout_value=conn.timeout)
                    raise
    ```
    
3. **에러 핸들링**:
    - 다양한 네트워크 관련 예외들을 캐치하고, 필요한 경우 프록시 에러로 포장하여 예외를 다시 발생시킵니다.
    
    ```python
    except (
                OSError,
                NewConnectionError,
                TimeoutError,
                BaseSSLError,
                CertificateError,
                SSLError,
            ) as e:
                new_e: Exception = e
                if isinstance(e, (BaseSSLError, CertificateError)):
                    new_e = SSLError(e)
                # If the connection didn't successfully connect to it's proxy
                # then there
                if isinstance(
                    new_e, (OSError, NewConnectionError, TimeoutError, SSLError)
                ) and (conn and conn.proxy and not conn.has_connected_to_proxy):
                    new_e = _wrap_proxy_error(new_e, conn.proxy.scheme)
                raise new_e
    ```
    
4. **요청 실행**:
    - **`conn.request(...)`**: 설정된 HTTP 메서드, URL, 본문 데이터, 헤더 등을 사용하여 실제 HTTP 요청을 보냄
    
    ```python
      try:
                conn.request(
                    method,
                    url,
                    body=body,
                    headers=headers,
                    chunked=chunked,
                    preload_content=preload_content,
                    decode_content=decode_content,
                    enforce_content_length=enforce_content_length,
                )
    ```
    
5. **응답 처리**:
    - **`response = conn.getresponse()`**: 서버로부터 응답을 받아옴
    - **`self._raise_timeout(err=e, url=url, timeout_value=read_timeout)`**: 읽기 타임아웃을 처리
    
    ```python
    try:
                response = conn.getresponse()
            except (BaseSSLError, OSError) as e:
                self._raise_timeout(err=e, url=url, timeout_value=read_timeout)
                raise
    ```
    
6. **응답 객체 설정**:
    - 재시도 횟수, 연결 객체, 연결 풀 등을 설정할 수 있습니다.
    
    ```python
    response.retries = retries
            response._connection = response_conn  # type: ignore[attr-defined]
            response._pool = self  # type: ignore[attr-defined
    ```
    
7. **응답 로깅**
    
    ```python
            # emscripten connection doesn't have _http_vsn_str
            http_version = getattr(conn, "_http_vsn_str", "HTTP/?")
            log.debug(
                '%s://%s:%s "%s %s %s" %s %s',
                self.scheme,
                self.host,
                self.port,
                method,
                url,
                # HTTP version
                http_version,
                response.status,
                response.length_remaining,
            )
    ```
    
8. **응답 반환**
    
    ```python
    return response
    ```
    

---

### **`close` 메서드**

이 메서드는 모든 풀링된 연결을 닫고 연결 풀을 비활성화합니다. 이는 리소스를 해제하고 잠재적인 메모리 누수를 방지하는 데 중요흠

```python
 def close(self) -> None:
        """
        Close all pooled connections and disable the pool.
        """
        if self.pool is None:
            return
        # Disable access to the pool
        old_pool, self.pool = self.pool, None

        # Close all the HTTPConnections in the pool.
        _close_pool_connections(old_pool)

    def is_same_host(self, url: str) -> bool:
        """
        Check if the given ``url`` is a member of the same host as this
        connection pool.
        """
        if url.startswith("/"):
            return True

        # TODO: Add optional support for socket.gethostbyname checking.
        scheme, _, host, port, *_ = parse_url(url)
        scheme = scheme or "http"
        if host is not None:
            host = _normalize_host(host, scheme=scheme)

        # Use explicit default port for comparison when none is given
        if self.port and not port:
            port = port_by_scheme.get(scheme)
        elif not self.port and port == port_by_scheme.get(scheme):
            port = None

        return (scheme, host, port) == (self.scheme, self.host, self.port)
```

- **`if self.pool is None:`**: 현재 연결 풀이 이미 **`None`**인지 확인합니다. 이 경우 메서드는 아무 작업 없이 반환합니다.
- **`old_pool, self.pool = self.pool, None`**: 연결 풀에 대한 접근을 비활성화하고, 기존 풀을 **`old_pool`** 변수에 저장합니다.
- **`_close_pool_connections(old_pool)`**: **`old_pool`**에 있는 모든 **`HTTPConnection`** 객체를 닫습니다. 이 부분은 실제 연결을 종료하는 작업을 수행합니다.

### **`is_same_host` 메서드**

이 메서드는 주어진 URL이 현재 연결 풀과 동일한 호스트에 속하는지를 확인합니다. 이는 요청을 보낼 때 연결 재사용 여부를 결정하는 데 사용됩니다.

- **`if url.startswith("/"):`**: URL이 상대 경로로 시작하는 경우, 현재 호스트와 동일한 것으로 간주하고 **`True`**를 반환합니다.
- URL 파싱과 호스트 정규화:
    - **`parse_url(url)`**: 주어진 URL을 파싱하여 구성 요소(스키마, 호스트, 포트 등)를 추출합니다.
    - **`scheme = scheme or "http"`**: 스키마가 지정되지 않은 경우 기본값으로 "http"를 사용합니다.
    - **`_normalize_host(host, scheme=scheme)`**: 호스트 이름을 정규화합니다(예: **`www.example.com`**과 **`example.com`**을 동일하게 처리).
- 포트 비교:
    - **`if self.port and not port:`**: URL에서 포트가 명시되지 않은 경우, 스키마에 따른 기본 포트를 사용합니다.
    - **`elif not self.port and port == port_by_scheme.get(scheme):`**: 연결 풀에 포트가 설정되지 않고 URL의 포트가 스키마의 기본 포트와 동일한 경우, 포트를 **`None`**으로 설정합니다.
- **`return (scheme, host, port) == (self.scheme, self.host, self.port)`**: 최종적으로 URL의 스키마, 호스트, 포트가 연결 풀의 해당 값과 일치하는지를 비교합니다.

---

### urlopen

```python
    def urlopen(  # type: ignore[override]
        self,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        headers: typing.Mapping[str, str] | None = None,
        retries: Retry | bool | int | None = None,
        redirect: bool = True,
        assert_same_host: bool = True,
        timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
        pool_timeout: int | None = None,
        release_conn: bool | None = None,
        chunked: bool = False,
        body_pos: _TYPE_BODY_POSITION | None = None,
        preload_content: bool = True,
        decode_content: bool = True,
        **response_kw: typing.Any,
    ) -> BaseHTTPResponse:
```

1. **method**:
    - HTTP 요청 메서드(예: GET, POST, PUT 등)를 지정합니다.
2. **url**:
    - 요청을 보낼 URL을 지정합니다.
3. **body**:
    - 요청 본문에 전송할 데이터를 지정합니다. 데이터 유형으로는 문자열, 바이트, 반복 가능한 문자열/바이트, 파일과 같은 객체가 포함될 수 있습니다.
4. **headers**:
    - 요청과 함께 보낼 사용자 정의 헤더의 딕셔너리입니다. 지정하지 않으면 연결 풀의 헤더가 사용됩니다.
5. **retries**:
    - 연결 오류 발생 시 재시도 횟수를 구성합니다. **`None`**은 기본적으로 3회 재시도하며, 정수를 지정하면 해당 횟수만큼 연결 오류에 대해 재시도합니다. **`False`**로 설정하면 재시도를 비활성화하고 예외가 즉시 발생합니다.
6. **redirect**:
    - **`True`**로 설정하면 자동으로 리디렉션(상태 코드 301, 302, 303, 307, 308)을 처리합니다. 각 리디렉션은 재시도로 계산됩니다.
7. **assert_same_host**:
    - **`True`**로 설정하면 요청이 이루어지는 호스트가 연결 풀의 호스트와 일치하는지 확인합니다. **`False`**로 설정하면 HTTP 프록시를 통해 외부 호스트로의 요청이 가능합니다.
8. **timeout**:
    - 요청에 대한 타임아웃을 지정합니다. 초 단위의 부동소수점 수 또는 **`urllib3.util.Timeout`** 인스턴스일 수 있습니다.
9. **pool_timeout**:
    - 연결 풀이 차단 모드로 설정되어 있고 사용 가능한 연결이 없을 경우, 이 메서드는 지정된 시간(초) 동안 차단 후 **`EmptyPoolError`** 예외를 발생시킵니다.
10. **preload_content**:
    - **`True`**로 설정하면 응답 본문을 메모리에 미리 로드합니다.
11. **decode_content**:
    - **`True`**로 설정하면 'content-encoding' 헤더에 따라 응답 본문을 디코드합니다.
12. **release_conn**:
    - **`False`**로 설정하면 응답을 받은 후 연결을 연결 풀에 반환하지 않습니다. **`None`**일 경우 **`preload_content`**의 값에 따라 결정되며, 기본적으로 **`True`**입니다.
13. **chunked**:
    - **`True`**로 설정하면 청크 전송 인코딩을 사용하여 본문을 전송합니다. 그렇지 않으면 표준 content-length 형식을 사용합니다.
14. **body_pos**:
    - 재시도나 리디렉션 시 파일과 같은 본문의 특정 위치로 이동하는 데 사용됩니다. 일반적으로 사용자가 설정할 필요는 없으며 **`urllib3`**가 필요에 따라 자동으로 값을 설정합니다.

---

### urlopen(2)

```python
parsed_url = parse_url(url)
        destination_scheme = parsed_url.scheme

        if headers is None:
            headers = self.headers

        if not isinstance(retries, Retry):
            retries = Retry.from_int(retries, redirect=redirect, default=self.retries)

        if release_conn is None:
            release_conn = preload_content

        # Check host
        if assert_same_host and not self.is_same_host(url):
            raise HostChangedError(self, url, retries)

        # Ensure that the URL we're connecting to is properly encoded
        if url.startswith("/"):
            url = to_str(_encode_target(url))
        else:
            url = to_str(parsed_url.url)

        conn = None

        # Track whether `conn` needs to be released before
        # returning/raising/recursing. Update this variable if necessary, and
        # leave `release_conn` constant throughout the function. That way, if
        # the function recurses, the original value of `release_conn` will be
        # passed down into the recursive call, and its value will be respected.
        #
        # See issue #651 [1] for details.
        #
        # [1] <https://github.com/urllib3/urllib3/issues/651>
        release_this_conn = release_conn

        http_tunnel_required = connection_requires_http_tunnel(
            self.proxy, self.proxy_config, destination_scheme
        )
```

1. **URL 파싱**:
    - **`parsed_url = parse_url(url)`**: 주어진 URL을 파싱하여 URL의 구성 요소(스키마, 호스트, 포트 등)를 분리합니다.
    - **`destination_scheme = parsed_url.scheme`**: 파싱된 URL에서 스키마(예: http, https)를 추출하여 변수에 저장합니다.
2. **헤더 설정**:
    - **`if headers is None: headers = self.headers`**: 사용자가 헤더를 제공하지 않았다면, 연결 풀의 기본 헤더를 사용합니다.
3. **재시도 설정**:
    - **`if not isinstance(retries, Retry):`**: 제공된 **`retries`**가 **`Retry`** 객체가 아닌 경우,
    - **`retries = Retry.from_int(retries, redirect=redirect, default=self.retries)`**: **`retries`**를 정수값으로부터 **`Retry`** 객체로 변환합니다. 이 때 리디렉션 설정과 기본 재시도 설정을 반영합니다.
4. **연결 해제 설정**:
    - **`if release_conn is None: release_conn = preload_content`**: **`release_conn`**이 명시되지 않았다면, **`preload_content`**의 값에 따라 결정됩니다. 이는 응답 내용을 미리 로드할 때 연결을 자동으로 해제할지 결정합니다.
5. **호스트 검사**:
    - **`if assert_same_host and not self.is_same_host(url):`**: **`assert_same_host`**가 참이고, 주어진 URL이 현재 연결 풀의 호스트와 다른 경우,
    - **`raise HostChangedError(self, url, retries)`**: **`HostChangedError`** 예외를 발생시킵니다. 이는 요청 호스트가 예상과 다를 때 오류를 나타냅니다.
6. **URL 인코딩 확인**:
    - **`if url.startswith("/"): url = to_str(_encode_target(url))`**: URL이 상대 경로로 시작하는 경우, URL을 인코드하여 문자열로 변환합니다.
    - **`else: url = to_str(parsed_url.url)`**: 그 외의 경우, 파싱된 URL을 문자열로 변환합니다.
7. **연결 트래킹 변수 설정**:
    - **`release_this_conn = release_conn`**: 이 변수는 함수 내에서 연결을 해제해야 할지 여부를 추적합니다. **`release_conn`**의 값을 변경하지 않고 일관성을 유지하기 위해 별도의 변수를 사용합니다.
8. **HTTP 터널 요구사항 확인**:
    - **`http_tunnel_required = connection_requires_http_tunnel(self.proxy, self.proxy_config, destination_scheme)`**: 프록시 설정과 목적지 스키마를 기반으로 HTTP 터널링이 필요한지 확인합니다. 이는 주로 보안 연결을 위한 프록시 사용 시 필요합니다.

---

### urlopen(3)

```python
 # Merge the proxy headers. Only done when not using HTTP CONNECT. We
        # have to copy the headers dict so we can safely change it without those
        # changes being reflected in anyone else's copy.
        if not http_tunnel_required:
            headers = headers.copy()  # type: ignore[attr-defined]
            headers.update(self.proxy_headers)  # type: ignore[union-attr]

        # Must keep the exception bound to a separate variable or else Python 3
        # complains about UnboundLocalError.
        err = None

        # Keep track of whether we cleanly exited the except block. This
        # ensures we do proper cleanup in finally.
        clean_exit = False

        # Rewind body position, if needed. Record current position
        # for future rewinds in the event of a redirect/retry.
        body_pos = set_file_position(body, body_pos)

        try:
            # Request a connection from the queue.
            timeout_obj = self._get_timeout(timeout)
            conn = self._get_conn(timeout=pool_timeout)

            conn.timeout = timeout_obj.connect_timeout  # type: ignore[assignment]

            # Is this a closed/new connection that requires CONNECT tunnelling?
            if self.proxy is not None and http_tunnel_required and conn.is_closed:
                try:
                    self._prepare_proxy(conn)
                except (BaseSSLError, OSError, SocketTimeout) as e:
                    self._raise_timeout(
                        err=e, url=self.proxy.url, timeout_value=conn.timeout
                    )
                    raise

            # If we're going to release the connection in ``finally:``, then
            # the response doesn't need to know about the connection. Otherwise
            # it will also try to release it and we'll have a double-release
            # mess.
            response_conn = conn if not release_conn else None

            # Make the request on the HTTPConnection object
            response = self._make_request(
                conn,
                method,
                url,
                timeout=timeout_obj,
                body=body,
                headers=headers,
                chunked=chunked,
                retries=retries,
                response_conn=response_conn,
                preload_content=preload_content,
                decode_content=decode_content,
                **response_kw,
            )

            # Everything went great!
            clean_exit = True

```

이 코드 조각은 HTTP 요청을 보내기 전에 여러 설정과 준비 단계를 처리하는 과정을 나타냅니다. 주로 연결을 관리하고, 프록시 설정을 적용하며, 예외 처리 및 요청 실행에 필요한 로직을 포함하고 있습니다. 각 단계별 기능은 다음과 같습니다:

1. **프록시 헤더 병합**:
    - **`if not http_tunnel_required:`**: HTTP CONNECT를 사용하지 않는 경우에만 프록시 헤더를 병합합니다.
    - **`headers = headers.copy()`**: 헤더 딕셔너리를 복사하여 원본에 영향을 주지 않도록 합니다.
    - **`headers.update(self.proxy_headers)`**: 프록시 헤더를 복사한 헤더 딕셔너리에 추가합니다. 이는 요청이 프록시를 통해 전송될 때 필요한 추가 헤더를 포함시키기 위함입니다.
2. **예외 처리 준비**:
    - **`err = None`**: 예외를 저장할 변수를 초기화합니다. 이는 나중에 예외가 발생했는지 판단하기 위해 사용됩니다.
    - **`clean_exit = False`**: 요청 처리 과정이 성공적으로 완료되었는지 추적하기 위한 플래그입니다.
3. **요청 본문 위치 설정**:
    - **`body_pos = set_file_position(body, body_pos)`**: 요청 본문이 파일이나 유사한 객체일 경우, 필요에 따라 읽기 위치를 조정합니다. 이는 리다이렉트나 재시도 발생 시 이전 위치로 돌아가기 위함입니다.
4. **연결 요청 및 설정**:
    - **`timeout_obj = self._get_timeout(timeout)`**: 요청에 사용할 타임아웃 객체를 가져옵니다.
    - **`conn = self._get_conn(timeout=pool_timeout)`**: 연결 풀에서 타임아웃 설정을 반영하여 연결을 요청합니다.
    - **`conn.timeout = timeout_obj.connect_timeout`**: 연결에 적용할 연결 타임아웃을 설정합니다.
5. **프록시 터널링 처리**:
    - **`if self.proxy is not None and http_tunnel_required and conn.is_closed:`**: 프록시를 사용하고, HTTP 터널링이 필요하며, 연결이 닫혀 있는 경우,
    - **`self._prepare_proxy(conn)`**: 프록시를 준비합니다. 예를 들어, HTTPS를 통한 프록시 연결 설정 등이 이에 해당합니다.
    - **`self._raise_timeout(err=e, url=self.proxy.url, timeout_value=conn.timeout)`**: 타임아웃이나 다른 네트워크 오류가 발생했을 때 적절한 예외를 발생시킵니다.
6. **응답 연결 관리**:
    - **`response_conn = conn if not release_conn else None`**: **`release_conn`**이 **`False`**인 경우, 응답 객체가 연결을 관리하도록 설정합니다. 이는 **`finally`** 블록에서 연결을 자동으로 해제하지 않을 경우 필요합니다.
7. **HTTP 요청 실행**:
    - **`response = self._make_request(...)`**: 설정된 파라미터를 사용하여 실제 HTTP 요청을 실행하고 응답을 받습니다.
8. **성공적 처리 표시**:
    - **`clean_exit = True`**: 요청이 성공적으로 처리되었음을 나타냅니다.

---

### urlopen(4)

```python
       except EmptyPoolError:
            # Didn't get a connection from the pool, no need to clean up
            clean_exit = True
            release_this_conn = False
            raise

        except (
            TimeoutError,
            HTTPException,
            OSError,
            ProtocolError,
            BaseSSLError,
            SSLError,
            CertificateError,
            ProxyError,
        ) as e:
            # Discard the connection for these exceptions. It will be
            # replaced during the next _get_conn() call.
            clean_exit = False
            new_e: Exception = e
            if isinstance(e, (BaseSSLError, CertificateError)):
                new_e = SSLError(e)
            if isinstance(
                new_e,
                (
                    OSError,
                    NewConnectionError,
                    TimeoutError,
                    SSLError,
                    HTTPException,
                ),
            ) and (conn and conn.proxy and not conn.has_connected_to_proxy):
                new_e = _wrap_proxy_error(new_e, conn.proxy.scheme)
            elif isinstance(new_e, (OSError, HTTPException)):
                new_e = ProtocolError("Connection aborted.", new_e)

            retries = retries.increment(
                method, url, error=new_e, _pool=self, _stacktrace=sys.exc_info()[2]
            )
            retries.sleep()

            # Keep track of the error for the retry warning.
            err = e

        finally:
            if not clean_exit:
                # We hit some kind of exception, handled or otherwise. We need
                # to throw the connection away unless explicitly told not to.
                # Close the connection, set the variable to None, and make sure
                # we put the None back in the pool to avoid leaking it.
                if conn:
                    conn.close()
                    conn = None
                release_this_conn = True

            if release_this_conn:
                # Put the connection back to be reused. If the connection is
                # expired then it will be None, which will get replaced with a
                # fresh connection during _get_conn.
                self._put_conn(conn)

        if not conn:
            # Try again
            log.warning(
                "Retrying (%r) after connection broken by '%r': %s", retries, err, url
            )
            return self.urlopen(
                method,
                url,
                body,
                headers,
                retries,
                redirect,
                assert_same_host,
                timeout=timeout,
                pool_timeout=pool_timeout,
                release_conn=release_conn,
                chunked=chunked,
                body_pos=body_pos,
                preload_content=preload_content,
                decode_content=decode_content,
                **response_kw,
            )
```

### **`except` 블록들**

1. **EmptyPoolError**:
    - 연결 풀에서 연결을 얻지 못한 경우, **`clean_exit`**를 **`True`**로 설정하고 **`release_this_conn`**을 **`False`**로 설정하여 이 함수에서 연결을 해제하지 않도록 합니다. 이 예외는 다시 발생되어 호출자에게 전달됩니다.
2. **다양한 네트워크 및 SSL 예외 처리**:
    - **`TimeoutError`**, **`HTTPException`**, **`OSError`**, **`ProtocolError`**, **`BaseSSLError`**, **`SSLError`**, **`CertificateError`**, **`ProxyError`** 등 다양한 예외들이 여기에서 처리됩니다.
    - 예외가 발생하면 **`clean_exit`**는 **`False`**로 설정됩니다.
    - 특정 예외 유형에 따라 새로운 예외 유형으로 변환될 수 있습니다. 예를 들어, **`BaseSSLError`**나 **`CertificateError`**는 **`SSLError`**로 변환됩니다.
    - 프록시를 사용하는 경우와 그렇지 않은 경우에 따라 다르게 처리될 수 있으며, 적절한 예외로 포장됩니다 (**`_wrap_proxy_error`**).
    - 예외가 발생하면 **`retries`** 객체를 사용하여 재시도 횟수를 증가시키고, 재시도 전에 지연(sleep)을 수행합니다.

### **`finally` 블록**

- **`finally`** 블록은 요청 수행 후 항상 실행됩니다. 여기서는 연결 관리와 관련된 정리 작업을 수행합니다.
- **`if not clean_exit`**: 예외가 발생했거나 다른 문제가 있었던 경우, 연결을 닫고 **`None`**으로 설정합니다. 필요한 경우 연결 풀에 **`None`**을 반환하여 연결 누수를 방지합니다.
- **`if release_this_conn`**: 연결을 해제해야 하는 경우 (**`release_conn`**이 **`True`**일 때), **`_put_conn`** 메서드를 호출하여 연결을 풀에 반환하거나 해제합니다.

### **재시도 로직**

- **`if not conn`**: 현재 연결이 없는 경우, 로그를 기록하고 **`self.urlopen`**을 호출하여 요청을 재시도합니다. 재시도 시에는 모든 원래 파라미터와 함께 몇 가지 추가 파라미터(**`body_pos`**, **`preload_content`**, **`decode_content`** 등)를 넘깁니다.

---

```python
 # Handle redirect?
        redirect_location = redirect and response.get_redirect_location()
        if redirect_location:
            if response.status == 303:
                # Change the method according to RFC 9110, Section 15.4.4.
                method = "GET"
                # And lose the body not to transfer anything sensitive.
                body = None
                headers = HTTPHeaderDict(headers)._prepare_for_method_change()

            try:
                retries = retries.increment(method, url, response=response, _pool=self)
            except MaxRetryError:
                if retries.raise_on_redirect:
                    response.drain_conn()
                    raise
                return response

            response.drain_conn()
            retries.sleep_for_retry(response)
            log.debug("Redirecting %s -> %s", url, redirect_location)
            return self.urlopen(
                method,
                redirect_location,
                body,
                headers,
                retries=retries,
                redirect=redirect,
                assert_same_host=assert_same_host,
                timeout=timeout,
                pool_timeout=pool_timeout,
                release_conn=release_conn,
                chunked=chunked,
                body_pos=body_pos,
                preload_content=preload_content,
                decode_content=decode_content,
                **response_kw,
            )

        # Check if we should retry the HTTP response.
        has_retry_after = bool(response.headers.get("Retry-After"))
        if retries.is_retry(method, response.status, has_retry_after):
            try:
                retries = retries.increment(method, url, response=response, _pool=self)
            except MaxRetryError:
                if retries.raise_on_status:
                    response.drain_conn()
                    raise
                return response

            response.drain_conn()
            retries.sleep(response)
            log.debug("Retry: %s", url)
            return self.urlopen(
                method,
                url,
                body,
                headers,
                retries=retries,
                redirect=redirect,
                assert_same_host=assert_same_host,
                timeout=timeout,
                pool_timeout=pool_timeout,
                release_conn=release_conn,
                chunked=chunked,
                body_pos=body_pos,
                preload_content=preload_content,
                decode_content=decode_content,
                **response_kw,
            )

        return response

```

### **리디렉션 처리**

1. **리디렉션 위치 파악**:
    - **`redirect_location = redirect and response.get_redirect_location()`**: 리디렉션이 활성화되어 있고, 응답에 리디렉션 위치가 있다면 해당 위치(URL)을 변수에 저장합니다.
2. **HTTP 303 See Other 대응**:
    - **`if response.status == 303:`**: 응답 상태 코드가 303(See Other)인 경우, 요청 메서드를 "GET"으로 변경하고, 요청 본문을 제거합니다. 이는 RFC 9110, 섹션 15.4.4에 따른 것입니다.
    - **`headers = HTTPHeaderDict(headers)._prepare_for_method_change()`**: 리디렉션으로 인해 요청 메서드가 변경될 때 적절한 헤더 변경을 수행합니다.
3. **리디렉션 재시도**:
    - **`retries = retries.increment(method, url, response=response, _pool=self)`**: 리디렉션을 시도하기 전에 재시도 횟수를 증가시킵니다.
    - **`response.drain_conn()`**: 응답으로부터 모든 데이터를 읽어 연결을 정리합니다.
    - **`retries.sleep_for_retry(response)`**: 리디렉션 전에 지정된 시간만큼 대기합니다.
    - 재귀적으로 **`self.urlopen`**을 호출하여 리디렉션된 위치로 새 요청을 보냅니다.

### **재시도 처리**

1. **재시도 가능 여부 확인**:
    - **`has_retry_after = bool(response.headers.get("Retry-After"))`**: 응답 헤더에 "Retry-After"가 있으면 재시도를 고려합니다.
    - **`if retries.is_retry(method, response.status, has_retry_after)`**: 주어진 조건에 따라 재시도가 필요한지 평가합니다.
2. **HTTP 응답 재시도**:
    - **`retries = retries.increment(method, url, response=response, _pool=self)`**: 재시도 카운터를 증가시키고,
    - **`response.drain_conn()`**: 연결에서 남은 데이터를 모두 읽어내고,
    - **`retries.sleep(response)`**: 서버가 지정한 대기 시간만큼 재시도 전에 대기합니다.
    - 재귀적으로 **`self.urlopen`**을 호출하여 동일 URL에 대한 요청을 재시도합니다.

### **요청 완료**

- 마지막에 **`return response`**를 통해 최종적으로 얻은 HTTP 응답을 반환합니다