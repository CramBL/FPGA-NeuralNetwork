library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

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
    signal mem : mem_array(0 to 2**inWidth-1);
    signal y_tmp   : STD_LOGIC_VECTOR(inWidth-1 downto 0);
begin

    initialize: process
    begin
        file file_ptr: text;
        variable line_buf: line;
        variable mem_val: STD_LOGIC_VECTOR(dataWidth-1 downto 0);
        variable mem_index: integer := 0;
        variable file_open: boolean := FALSE;
        variable read_success: boolean := TRUE;

        file_open := file_open(file_ptr, "sigContent.mif", READ_MODE);
        if file_open then
            while not endfile(file_ptr) loop
                readline(file_ptr, line_buf);
                read(line_buf, mem_val);
                mem(mem_index) <= mem_val;
                mem_index := mem_index + 1;
            end loop;
            file_close(file_ptr);
        else
            report "Error opening sigContent.mif file" severity failure;
        end if;

        wait;
    end process initialize;
    
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
    
    y_out <= mem(to_integer(unsigned(y_out)));
    
end architecture behavioral;
