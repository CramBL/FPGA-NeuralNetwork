library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use std.textio.all;

entity Sig_ROM_VHDL is
    generic (
        inWidth  : integer := 10;
        dataWidth: integer := 16
    );
    port (
        clk : in STD_LOGIC;
        x   : in STD_LOGIC_VECTOR(inWidth-1 downto 0);
        y_out : out STD_LOGIC_VECTOR(dataWidth-1 downto 0)
    );
end entity Sig_ROM_VHDL;

                                                       


architecture behavioral of Sig_ROM_VHDL is
    type mem_array is array (natural range <>) of STD_LOGIC_VECTOR(dataWidth-1 downto 0);
    -- Vivado is terrible, this doesn't work: 
    -- https://support.xilinx.com/s/question/0D52E00006hpdz4SAA/file-integer-read-size-mismatch-in-assignment-read-failed?language=en_US
    impure function init_ram_bin return mem_array is
      file text_file : text open read_mode is "sigContent.mif";
      variable text_line : line;
      variable ram_content : mem_array(0 to 2**inWidth-1);
    begin
      for i in 0 to (2**inWidth-1-1) loop
        readline(text_file, text_line);
        bread(text_line, ram_content(i));
      end loop;
      return ram_content;
    end function;
    signal mem : mem_array(0 to 2**inWidth-1) := init_ram_bin;
    signal y_tmp   : STD_LOGIC_VECTOR(inWidth-1 downto 0);
begin

    process(clk)
    
    
    
    
    begin
        if rising_edge(clk) then
            if signed(x) >= 0 then
                y_tmp <= STD_LOGIC_VECTOR(unsigned(x) + 2**(inWidth-1));
            else
                y_tmp <= STD_LOGIC_VECTOR(unsigned(x) - 2**(inWidth-1));
            end if;
        end if;
    end process;
    
    y_out <= mem(to_integer(unsigned(y_tmp)));
    
end architecture behavioral;
