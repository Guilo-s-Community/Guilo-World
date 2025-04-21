defmodule Helloteste.Endpoint do
  use GRPC.Endpoint

  intercept GRPC.Server.Interceptors.Logger
  run Helloteste.Greeter.Server
end
