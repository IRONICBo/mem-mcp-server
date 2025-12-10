# typed: false
# frozen_string_literal: true

class Mem < Formula
  desc "AI-powered version control tool - memory layer for AI coding agents"
  homepage "https://github.com/IRONICBo/mem-mcp-server"
  version "0.0.6"
  license "MIT"

  on_macos do
    if Hardware::CPU.intel?
      url "https://github.com/IRONICBo/mem-mcp-server/releases/download/v0.0.6/mem-macos-x86_64.tar.gz"
      sha256 "37f7797a8a05e9b7153d46446ec88fa4e63e96af6a111a9afa7c4d26c7fd000f"
    end
    if Hardware::CPU.arm?
      url "https://github.com/IRONICBo/mem-mcp-server/releases/download/v0.0.6/mem-macos-arm64.tar.gz"
      sha256 "2ab7d0b654b5e0040aa2595d042cd5fbf7fe783ef18970fa2cb1724ab2bf90cf"
    end
  end

  on_linux do
    if Hardware::CPU.intel? && Hardware::CPU.is_64_bit?
      url "https://github.com/IRONICBo/mem-mcp-server/releases/download/v0.0.6/mem-linux-x86_64.tar.gz"
      sha256 "181d8a053ccfde9a49175b4bcfd13b55a55c58bc381815c44047d65b951c6315"
    end
  end

  def install
    if OS.mac?
      if Hardware::CPU.intel?
        bin.install "mem-macos-x86_64" => "mem"
      else
        bin.install "mem-macos-arm64" => "mem"
      end
    else
      bin.install "mem-linux-x86_64" => "mem"
    end
  end

  test do
    system "\#{bin}/mem", "--help"
  end
end
