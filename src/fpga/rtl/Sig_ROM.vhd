library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Sig_ROM_VHDL is
    generic (
        inWidth  : integer := 10;
        dataWidth: integer := 16
    );
    port (
        clk : in std_logic;
        x   : in std_logic_vector(inWidth-1 downto 0);
        out : out std_logic_vector(dataWidth-1 downto 0)
    );
end entity Sig_ROM_VHDL;

architecture behavioral of Sig_ROM_VHDL is
    type mem_array is array (natural range <>) of std_logic_vector(dataWidth-1 downto 0);
    signal mem : mem_array(0 to 2**inWidth-1);
    signal y   : std_logic_vector(inWidth-1 downto 0);
begin

    initialize: process
    begin
        file file_ptr: text;
        variable line_buf: line;
        variable mem_val: std_logic_vector(dataWidth-1 downto 0);
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
                y <= std_logic_vector(unsigned(x) + 2**(inWidth-1));
            else
                y <= std_logic_vector(unsigned(x) - 2**(inWidth-1));
            end if;
        end if;
    end process;
    
    out <= mem(to_integer(unsigned(y)));
    
end architecture behavioral;
