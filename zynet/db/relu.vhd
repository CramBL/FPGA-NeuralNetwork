library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use IEEE.STD_LOGIC_MISC.ALL;



entity ReLU_VHDL is
    generic (
        dataWidth : integer := 16;
        weightIntWidth : integer := 4
    );
    port (
        clk : in STD_LOGIC;
        x : in STD_LOGIC_VECTOR(2*dataWidth-1 downto 0);
        y_out : out STD_LOGIC_VECTOR(dataWidth-1 downto 0)
    );
end entity ReLU_VHDL;

architecture Behavioral of ReLU_VHDL is
constant all_ones : std_logic_vector(x(2*dataWidth-1 downto weightIntWidth)'range) := (others => '1');
begin
    process (clk)
        --variable all_ones : std_logic_vector(2*dataWidth-1 downto 0);
    begin
        if rising_edge(clk) then
            if signed(x) >= 0 then
                if or(x(2*dataWidth-1 downto (2*dataWidth - weightIntWidth))) then -- overflow to sign bit of integer part
                    y_out <= ('0' & (dataWidth-2 downto 0 => '1')); -- Maximum value unsigned integer
                else
                    y_out <= x(2*dataWidth-1-weightIntWidth downto dataWidth-weightIntWidth);
                end if;
            else
                y_out <= (others => '0');
            end if;
        end if;
    end process;
end architecture Behavioral;