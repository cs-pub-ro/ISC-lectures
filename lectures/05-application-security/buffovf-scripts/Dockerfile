# Buffer-overflow lab env for ../buffovf-demo.md
#
#   docker build -t buffovf ./lectures/05-application-security/buffovf-scripts
#   docker run -it buffovf
#
# Inside:
#   - gcc + gcc-multilib  -> `make` builds vuln64 and vuln32
#   - gdb + pwndbg        -> checksec / cyclic / telescope / got / plt
#   - pwntools            -> exploit_ret2win.py, exploit_ret2libc_*.py, libc_leak.py
#   - labvm dotfiles      -> zsh (default shell), nvim, tmux, fzf

FROM debian:13

# Toolchain + debugger + dotfiles prerequisites.
# gcc-multilib: 32-bit targets (vuln32); libc6-dbg: libc symbols for gdb.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential unzip git rsync wget curl ca-certificates \
        zsh tmux fzf fd-find ripgrep \
        gdb gdbserver \
        gcc-multilib libc6-dbg \
        python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Latest official neovim (prebuilt, self-contained) — needed by the dotfiles
RUN wget -qO- https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz \
    | tar -xz -C /usr/local --strip-components=1

# pwndbg: setup.sh creates its own venv and writes /root/.gdbinit
RUN git clone --depth 1 https://github.com/pwndbg/pwndbg /opt/pwndbg \
    && cd /opt/pwndbg && ./setup.sh

# pwntools for the exploit scripts (Debian 13 pip is PEP-668 managed)
RUN python3 -m pip install --break-system-packages pwntools \
    && rm -rf /root/.cache/pip

# Lab VM dotfiles: zsh, nvim (astronvim), tmux, fzf, bash
RUN git clone --depth 1 https://github.com/cs-pub-ro/labvm-dotfiles /opt/dotfiles \
    && cd /opt/dotfiles && ./install.sh

# zsh as the default shell and entrypoint
RUN usermod -s /usr/bin/zsh root
CMD ["/usr/bin/zsh"]
