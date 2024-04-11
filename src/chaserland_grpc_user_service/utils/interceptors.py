import logging
import time
from collections.abc import AsyncIterator, Callable
from typing import Any

import grpc
from grpc_interceptor.exceptions import GrpcException
from grpc_interceptor.server import AsyncServerInterceptor


class AsyncAccessLoggerInterceptor(AsyncServerInterceptor):
    def __init__(self, logger: logging.Logger = logging.getLogger("grpc.access")):
        self.logger = logger

    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ):
        start_time = time.perf_counter() * 1000
        try:
            response_or_iterator = await method(request_or_iterator, context)
            if hasattr(response_or_iterator, "__aiter__"):
                return self._intercept_streaming(
                    response_or_iterator, context, start_time, method_name
                )
            return await response_or_iterator
        finally:
            endtime = time.perf_counter() * 1000
            elapsed_time = endtime - start_time
            status_code = (
                grpc.StatusCode(context.code())
                if context.code()
                else grpc.StatusCode.OK
            )
            self.logger.info(
                f'{context.peer()} - "{method_name}" {status_code.value[0]} {status_code.name} {elapsed_time:.2f}ms'
            )

    async def _intercept_streaming(self, iterator, context: grpc.ServicerContext):
        try:
            async for r in iterator:
                yield r
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise


class AsyncExceptionToStatusInterceptor(AsyncServerInterceptor):
    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ) -> Any:
        try:
            response_or_iterator = await method(request_or_iterator, context)
            if hasattr(response_or_iterator, "__aiter__"):
                return self._intercept_streaming(response_or_iterator, context)
            return await response_or_iterator
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            raise

    async def _intercept_streaming(
        self, iterator: AsyncIterator, context: grpc.ServicerContext
    ):
        try:
            async for r in iterator:
                yield r
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            raise
