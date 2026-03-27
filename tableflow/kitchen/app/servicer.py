from app.generated import kitchen_pb2
from app.generated import kitchen_pb2_grpc

_queue: dict[int, str] = {}

_TRANSITIONS: dict[str, set[str]] = {
    "received": {"preparing", "cancelled"},
    "preparing": {"ready", "cancelled"},
    "ready": {"delivered", "cancelled"},
    "delivered": set(),
    "cancelled": set(),
}


class KitchenServicer(kitchen_pb2_grpc.KitchenServiceServicer):

    def SubmitOrder(self, request, context):
        if request.order_id not in _queue:
            _queue[request.order_id] = "received"

        return kitchen_pb2.OrderAck(order_id=request.order_id, accepted=True)

    def UpdateOrderStatus(self, request, context):
        current_status = _queue.get(request.order_id)

        if not current_status:
            return kitchen_pb2.StatusResponse(
                order_id=request.order_id, status=request.status, success=False
            )

        if request.status not in _TRANSITIONS.get(current_status, set()):
            return kitchen_pb2.StatusResponse(
                order_id=request.order_id, status=request.status, success=False
            )

        _queue[request.order_id] = request.status

        return kitchen_pb2.StatusResponse(
            order_id=request.order_id, status=request.status, success=True
        )
