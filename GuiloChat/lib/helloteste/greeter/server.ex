defmodule Helloteste.Greeter.Server do
  use GRPC.Server, service: Helloteste.Greeter.Service

  @spec say_hello(Helloteste.HelloRequest.t(), GRPC.Server.Stream.t()) ::
          Helloteste.HelloReply.t()
  def say_hello(%Helloteste.HelloRequest{name: name}, _stream) do
    IO.puts("Recebido: #{name}")
    %Helloteste.HelloReply{message: "Olá, #{name}!"}
  end
end
