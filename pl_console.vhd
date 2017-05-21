library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;

entity pl_console is
    port(
        RESET : In std_logic;
        user_clk : In std_logic;
        user_wren : In std_logic;
        user_rden : In std_logic;
        UART_CTL : Out std_logic;
        UART_BUSY : In std_logic;
        UART_DATA : Out std_logic_vector(7 DOWNTO 0);
        MOTOR_1 : Out std_logic_vector(15 DOWNTO 0);
        MOTOR_2 : Out std_logic_vector(15 DOWNTO 0);
        MOTOR_3 : Out std_logic_vector(15 DOWNTO 0);
        MOTOR_4 : Out std_logic_vector(15 DOWNTO 0);
        MOTOR_5 : Out std_logic_vector(15 DOWNTO 0);
        MOTOR_6 : Out std_logic_vector(15 DOWNTO 0);
        user_wstrb : In std_logic_vector(3 DOWNTO 0);
        user_wr_data : In std_logic_vector(31 DOWNTO 0);
        user_addr : In std_logic_vector(31 DOWNTO 0);
        user_rd_data : Out std_logic_vector(31 DOWNTO 0);
        GPIO_LED : OUT std_logic_vector(3 DOWNTO 0)
    );
end entity;

architecture beh of pl_console is
    type demo_mem is array(0 TO 31) of std_logic_vector(7 DOWNTO 0);    
    signal lite_addr : integer range 0 to 31;
    signal motor1 : std_logic_vector(15 DOWNTO 0);
    signal motor2 : std_logic_vector(15 DOWNTO 0);
    signal motor3 : std_logic_vector(15 DOWNTO 0);
    signal motor4 : std_logic_vector(15 DOWNTO 0);
    signal motor5 : std_logic_vector(15 DOWNTO 0);
    signal motor6 : std_logic_vector(15 DOWNTO 0);

    signal litearray0 : demo_mem;
    signal litearray1 : demo_mem;
    signal litearray2 : demo_mem;
    signal litearray3 : demo_mem;
begin
    lite_addr <= conv_integer(user_addr(6 DOWNTO 2));
    process(RESET,user_clk,UART_BUSY)
        type StateType is(S0,S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,S14,S15,S16);
        variable state : StateType := S0;
    begin
        if RESET = '0' then
            state:= S0;
            UART_CTL <= '0';
        elsif rising_edge(user_clk) then
            case state is
                when S0 =>
                    UART_CTL <= '0';
                    UART_DATA <= x"00";
                    state := S1;
                    
                    
                when S1 =>
                    UART_DATA <= motor1(15 DOWNTO 8);
                    state := S2;
                when S2 =>
                    UART_CTL <= '1';
                    state := S3;                    
                when S3 =>
                    UART_CTL <= '1';
                    state := S4;
                when S4 =>
                    if UART_BUSY = '1' then
                        UART_CTL <= '0';
                        state := S5;
                    end if;
                    
                when S5 =>
                    UART_DATA <= motor1(7 DOWNTO 0);
                    state := S6;
                when S6 =>
                    UART_CTL <= '1';
                    state := S7;                    
                when S7 =>
                    UART_CTL <= '1';
                    state := S8;
                when S8=>
                    if UART_BUSY = '1' then
                        UART_CTL <= '0';
                        state := S9;
                    end if;                                               
                    
                when S9 =>
                    UART_DATA <= motor6(15 DOWNTO 8);
                    state := S10;
                when S10 =>
                    UART_CTL <= '1';
                    state := S11;                    
                when S11 =>
                    UART_CTL <= '1';
                    state := S12;
                when S12 =>
                    if UART_BUSY = '1' then
                        UART_CTL <= '0';
                        state := S13;
                    end if; 
                    
                                        
                when S13 =>
                    UART_DATA <= motor6(7 DOWNTO 0);
                    state := S14;
                when S14 =>
                    UART_CTL <= '1';
                    state := S15;
                when S15 =>
                    UART_CTL <= '1';
                    state := S16;                     
                when S16 =>
                    if UART_BUSY = '1' then
                        UART_CTL <= '0';
                        state := S0;
                    end if;
                    
                when others =>
                    state := S0;        
            end case;
        end if;
        
    end process;
    process (user_clk)
            variable sys_status : std_logic_vector(31 DOWNTO 0);
    begin
        if (user_clk'event and user_clk = '1') then
                    if (user_wstrb(0) = '1') then 
          litearray0(lite_addr) <= user_wr_data(7 DOWNTO 0);
        end if;
    
        if (user_wstrb(1) = '1') then 
          litearray1(lite_addr) <= user_wr_data(15 DOWNTO 8);
        end if;
    
        if (user_wstrb(2) = '1') then 
          litearray2(lite_addr) <= user_wr_data(23 DOWNTO 16);
        end if;
    
        if (user_wstrb(3) = '1') then 
          litearray3(lite_addr) <= user_wr_data(31 DOWNTO 24);
        end if;
    
        if (user_rden = '1') then
          user_rd_data <= litearray3(lite_addr) & litearray2(lite_addr) &
                          litearray1(lite_addr) & litearray0(lite_addr);
        end if;
        
        
          if (lite_addr = 1) then
            GPIO_LED <= user_wr_data(31 DOWNTO 28);
            motor1 <= litearray3(lite_addr) & litearray2(lite_addr);      
          end if;
          if (lite_addr = 2) then
            motor2 <= litearray3(lite_addr) & litearray2(lite_addr);       
          end if;         
          if (lite_addr = 3) then
            motor3 <= litearray3(lite_addr) & litearray2(lite_addr);       
          end if;           
          if (lite_addr = 4) then
            motor4 <= litearray3(lite_addr) & litearray2(lite_addr);        
          end if;           
          if (lite_addr = 5) then
            motor5 <= litearray3(lite_addr) & litearray2(lite_addr);        
          end if; 
          if (lite_addr = 6) then
            motor6 <= litearray3(lite_addr) & litearray2(lite_addr);        
          end if;
          MOTOR_1 <= motor1;
          MOTOR_2 <= motor2;
          MOTOR_3 <= motor3;
          MOTOR_4 <= motor4;
          MOTOR_5 <= motor5;
          MOTOR_6 <= motor6;                     
--        GPIO_LED <= "0101";
--        if (user_clk'event and user_clk = '1') then
--            if (user_wren = '1') then
----              litearray(lite_addr) <= user_wr_data;
--                sys_status := user_wr_data;
--            end if;
--            if (user_rden = '1') then
----              user_rd_data <= litearray(lite_addr);
--                user_rd_data <= sys_status;
--            end if;
--        end if;
    end if;
    end process;
end architecture;
