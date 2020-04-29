# This file is Copyright (c) 2015 Yann Sionneau <yann.sionneau@gmail.com>
# This file is Copyright (c) 2015-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# This file is Copyright (c) 2020 Tom Keddie <github@bronwenandtom.com>
# License: BSD

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, VivadoProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("clk100", 0,
        Subsignal("p", Pins("Y18")),
        Subsignal("n", Pins("Y19")),
        IOStandard("LVDS_25")),
    ("flash", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("mosi", Pins("P22")),
        Subsignal("miso", Pins("R22")),
        Subsignal("vpp", Pins("P21")),
        Subsignal("hold", Pins("R21")),
        IOStandard("LVCMOS33")
    ),
    ("spiflash4x", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("dq", Pins("P22 R22 P21 R21")),
        IOStandard("LVCMOS33")
    ),
    ("serial", 0,
        Subsignal("tx", Pins("W17"), Misc("PULLUP=TRUE")),
        Subsignal("rx", Pins("W20")),
        IOStandard("LVCMOS33"),
    ),
    ("serial2", 0,
        Subsignal("tx", Pins("V17"), Misc("PULLUP=TRUE")),
        Subsignal("rx", Pins("W19")),
        IOStandard("LVCMOS33"),
    ),
    ("usb_a", 0,
     Subsignal("d_p", Pins("P19")),    # IO_L10_16_P
     Subsignal("d_n", Pins("R19")),    # IO_L10_16_N
     Subsignal("pullup", Pins("P20")), # IO_L8_16_N
     IOStandard("LVCMOS33")
    ),
    ("usb_micro", 0,
     Subsignal("d_p", Pins("V18")),    # IO_L10_16_P
     Subsignal("d_n", Pins("V19")),    # IO_L10_16_N
     Subsignal("pullup", Pins("U18")), # IO_L8_16_N
     Subsignal("id", Pins("U20")), # IO_L8_16_N
     IOStandard("LVCMOS33")
    ),
    ("user_btn_n", 0, Pins("U17"), IOStandard("LVCMOS33"), Misc("PULLUP=TRUE")),
    ("user_led_n", 0, Pins("P16"), IOStandard("LVCMOS33")),
    ("rgb_led_n", 0,
        Subsignal("r", Pins("P15")),  # IO_L7_13_P
        Subsignal("g", Pins("P16")),  # IO_L7_13_N
        Subsignal("b", Pins("P14")),  # IO_L8_13_N
        IOStandard("LVCMOS33"),
    ),
    ("pcie_ctrl", 0,
     Subsignal("wake", Pins("R16")),
     Subsignal("perst", Pins("R17")),
               IOStandard("LVCMOS33")),
    ("clk_i2c", 0,
     Subsignal("scl", Pins("N17"), IOStandard("LVCMOS33")),
     Subsignal("sda", Pins("P17"), IOStandard("LVCMOS33")),
     ),
    ("S0", 0,
     Subsignal("tx_p", Pins("B4")),
     Subsignal("tx_n", Pins("A4")),
     Subsignal("rx_p", Pins("B8")),
     Subsignal("rx_n", Pins("A8")),
     Subsignal("clk_p", Pins("F6"), IOStandard("LVDS_25")),
     Subsignal("clk_n", Pins("E6"), IOStandard("LVDS_25")),
    ),
    ("S2", 0,
     Subsignal("tx_p", Pins("B6")),
     Subsignal("tx_n", Pins("A6")),
     Subsignal("rx_p", Pins("B10")),
     Subsignal("rx_n", Pins("A10")),
     Subsignal("clk_p", Pins("F10"), IOStandard("LVDS_25")),
     Subsignal("clk_n", Pins("E10"), IOStandard("LVDS_25")),
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("j1_35", "A1 B1 D1 E1 G1 F1 J2 K2 K1 J1 L1 M1 N2 P2"),
    ("j1_34", "R2 R3 U1 T1 V2 U2 Y1 W1 Y2 W2 AB1 AA1 AB2 AB3"),
    ("j2_14", "AB18 AA18 AB20 AA19 AB22 AB21 AA21 AA20 Y22 Y21 W22 W21 U21 T21"),
    ("j2_16", "G22 G21 D22 E22 B22 C22 B21 A21 B17 B18 A19 A18 A15 A16"),
    ("tp",    "C2 B2 AB5 AA5 B15 B16 V22 V20"),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxPlatform):
    default_clk_name   = "clk100"
    default_clk_period = 1e9/100e6

    def __init__(self, variant="a7-15"):
        device = {
            "a7-15": "xc7a15t-fgg484-1",
            "a7-35": "xc7a35t-fgg484-1",
            "a7-50": "xc7a50t-fgg484-1",
        }[variant]
        XilinxPlatform.__init__(self, device, _io, _connectors, toolchain="vivado")
        self.toolchain.bitstream_commands = \
            ["set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]"]
        self.toolchain.additional_commands = \
            ["write_cfgmem -force -format bin -interface spix4 -size 16 "
             "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin"]

    def create_programmer(self):
        return VivadoProgrammer(flash_part="mx25l51245g-spi-x1_x2_x4")
