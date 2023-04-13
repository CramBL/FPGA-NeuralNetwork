library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity ReLU is
    generic (
        dataWidth : integer := 16;
        weightIntWidth : integer := 4
    );
    port (
        clk : in STD_LOGIC;
        x : in STD_LOGIC_VECTOR(2*dataWidth-1 downto 0);
        out : out STD_LOGIC_VECTOR(dataWidth-1 downto 0)
    );
end entity ReLU;

architecture Behavioral of ReLU is
begin
    process (clk)
    begin
        if rising_edge(clk) then
            if signed(x) >= 0 then
                if x(2*dataWidth-1 downto weightIntWidth) = (others => '1') then -- overflow to sign bit of integer part
                    out <= (others => '0') & ('1' & (dataWidth-1 downto 1 => '1'));
                else
                    out <= x(2*dataWidth-1-weightIntWidth downto dataWidth);
                end if;
            else
                out <= (others => '0');
            end if;
        end if;
    end process;
end architecture Behavioral;
