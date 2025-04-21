defmodule Httpserver.Application do
  use Application

  def start(_type, _args) do
    children = [
      # Inicia o servidor gRPC na porta 50051
      {GRPC.Server.Supervisor, endpoint: Helloteste.Endpoint, port: 50051}
    ]

    opts = [strategy: :one_for_one, name: Httpserver.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
