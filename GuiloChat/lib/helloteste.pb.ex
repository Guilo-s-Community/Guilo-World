defmodule Helloteste.HelloRequest do
  @moduledoc false
  use Protobuf, protoc_gen_elixir_version: "0.14.1", syntax: :proto3

  field :name, 1, type: :string
end

defmodule Helloteste.HelloReply do
  @moduledoc false
  use Protobuf, protoc_gen_elixir_version: "0.14.1", syntax: :proto3

  field :message, 1, type: :string
end

defmodule Helloteste.Greeter.Service do
  @moduledoc false

  use GRPC.Service, name: "helloteste.Greeter", protoc_gen_elixir_version: "0.14.1"

  rpc :SayHello, Helloteste.HelloRequest, Helloteste.HelloReply
end

defmodule Helloteste.Greeter.Stub do
  @moduledoc false

  use GRPC.Stub, service: Helloteste.Greeter.Service
end
