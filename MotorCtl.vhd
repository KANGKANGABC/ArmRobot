----------------------------------------------------------------------------------
-- Company: 
-- Engineer: ZhaoKang
-- 
-- Create Date: 2017/05/31 21:54:01
-- Design Name: 
-- Module Name: MotorCtl - beh
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functns with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity MotorCtl is
    Port ( 
           CLK : in STD_LOGIC;
           RESET : in STD_LOGIC;
           UART_TX : out STD_LOGIC;
           M1_degree : in STD_LOGIC_VECTOR (15 downto 0);
           M2_degree : in STD_LOGIC_VECTOR (15 downto 0);
           M3_degree : in STD_LOGIC_VECTOR (15 downto 0);
           M4_degree : in STD_LOGIC_VECTOR (15 downto 0);
           M5_degree : in STD_LOGIC_VECTOR (15 downto 0);
           M6_degree : in STD_LOGIC_VECTOR (15 downto 0)
           --TMP : buffer STD_LOGIC_VECTOR (15 downto 0)
           );
end entity;

architecture beh of MotorCtl is

component crc is
port ( 
      clk: in std_logic;
      data_in: in std_logic_vector(7 downto 0);
      crc_in: in std_logic_vector(15 downto 0);            
      crc_out: out std_logic_vector(15 downto 0)
      );
end component;

component UART_TX_CTRL is
port ( 
       SEND : in  STD_LOGIC;
       DATA : in  STD_LOGIC_VECTOR (7 downto 0);
       CLK : in  STD_LOGIC;
       READY : out  STD_LOGIC;
       UART_TX : out  STD_LOGIC
           );
end component;

--component InstructionRam is
--PORT (
--      clka : IN STD_LOGIC;
--      wea : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
--      addra : IN STD_LOGIC_VECTOR(6 DOWNTO 0);
--      dina : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
--      douta : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
--      clkb : IN STD_LOGIC;
--      web : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
--      addrb : IN STD_LOGIC_VECTOR(6 DOWNTO 0);
--      dinb : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
--      doutb : OUT STD_LOGIC_VECTOR(7 DOWNTO 0)
--      );
--end component;

SIGNAL clk_1 : std_logic;
SIGNAL crc_ret : std_logic_vector (15 downto 0);
SIGNAL crc_int : std_logic_vector (15 downto 0);
SIGNAL crc_data : std_logic_vector (7 downto 0);
--SIGNAL wea : std_logic_vector (0 downto 0);
--SIGNAL addra : std_logic_vector (6 downto 0);
--SIGNAL addrb : std_logic_vector (6 downto 0);
--SIGNAL dina : std_logic_vector (7 downto 0);
--SIGNAL douta : std_logic_vector (7 downto 0);
--SIGNAL dinb : std_logic_vector (7 downto 0);
--SIGNAL doutb : std_logic_vector (7 downto 0);

TYPE matrix_index is array (13 downto 0) of std_logic_vector(7 downto 0);
TYPE StateType is (S000,S00, S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, 
S15, S16, S17, S18, S19, S20, S21, S22, S23);
SIGNAL m1, m2, m3, m4, m5, m6 : matrix_index;
SIGNAL m1a, m2a, m3a, m4a, m5a, m6a : matrix_index;
signal UartBusy : std_logic;
signal UartCtl : std_logic;
signal UartData : std_logic_vector(7 DOWNTO 0);

begin
    crc_ins : crc
    port map(
      clk => clk_1,
      data_in => crc_data,
      crc_in =>  crc_int,
      crc_out =>  crc_ret
    );
    
    UART_TX_CTRL_ins : UART_TX_CTRL
    port map(
      READY => UartBusy,
      UART_TX => UART_TX,
      CLK => clk_1,
      DATA => UartData,
      SEND => UartCtl
    );
--    InstructionRam_ins : InstructionRam
--    port map(
--       clka => clk_1,
--       clkb => clk_1,
--       wea => wea,
--       web => wea,
--       addra => addra,
--       addrb => addrb,
--       dina => dina,
--       douta => douta,
--       dinb => dinb,
--       doutb => doutb        
--    );

    process(CLK)
        variable state : StateType := S000;
        variable count1 : integer range 0 to 13;
        variable TMP : std_logic_vector (15 downto 0);
    begin
--    m1(12) <= x"FF";m2(12) <= x"FF";m3(12) <= x"FF";m4(12) <= x"FF";m5(12) <= x"FF";m6(12) <= x"FF";
--    m1(13) <= x"FF";m2(13) <= x"FF";m3(13) <= x"FF";m4(13) <= x"FF";m5(13) <= x"FF";m6(13) <= x"FF";
        clk_1 <= CLK;
        if RESET = '0' then
            count1 := 0;
            state := S000;
        elsif falling_edge(CLK) then
            case state is
                when S000 =>
                    m1(0) <= x"FF";m2(0) <= x"FF";m3(0) <= x"FF";m4(0) <= x"FF";m5(0) <= x"FF";m6(0) <= x"FF";
                    m1(1) <= x"FF";m2(1) <= x"FF";m3(1) <= x"FF";m4(1) <= x"FF";m5(1) <= x"FF";m6(1) <= x"FF";
                    m1(2) <= x"FD";m2(2) <= x"FD";m3(2) <= x"FD";m4(2) <= x"FD";m5(2) <= x"FD";m6(2) <= x"FD";
                    m1(3) <= x"00";m2(3) <= x"00";m3(3) <= x"00";m4(3) <= x"00";m5(3) <= x"00";m6(3) <= x"00";
                    m1(4) <= x"01";m2(4) <= x"02";m3(4) <= x"03";m4(4) <= x"04";m5(4) <= x"05";m6(4) <= x"06";
                    
                    m1(5) <= x"07";m2(5) <= x"07";m3(5) <= x"07";m4(5) <= x"07";m5(5) <= x"07";m6(5) <= x"07";
                    m1(6) <= x"00";m2(6) <= x"00";m3(6) <= x"00";m4(6) <= x"00";m5(6) <= x"00";m6(6) <= x"00";
                    m1(7) <= x"03";m2(7) <= x"03";m3(7) <= x"03";m4(7) <= x"03";m5(7) <= x"03";m6(7) <= x"03";
                    m1(8) <= x"1E";m2(8) <= x"1E";m3(8) <= x"1E";m4(8) <= x"1E";m5(8) <= x"1E";m6(8) <= x"1E";
                    m1(9) <= x"00";m2(9) <= x"00";m3(9) <= x"00";m4(9) <= x"00";m5(9) <= x"00";m6(9) <= x"00";
                    m1(10) <= M1_degree(7 DOWNTO 0);m2(10) <= M2_degree(7 DOWNTO 0);m3(10) <= M3_degree(7 DOWNTO 0);
                    m4(10) <= M4_degree(7 DOWNTO 0);m5(10) <= M5_degree(7 DOWNTO 0);m6(10) <= M6_degree(7 DOWNTO 0);
                    m1(11) <= M1_degree(15 DOWNTO 8);m2(11) <= M2_degree(15 DOWNTO 8);m3(11) <= M3_degree(15 DOWNTO 8);
                    m4(11) <= M4_degree(15 DOWNTO 8);m5(11) <= M5_degree(15 DOWNTO 8);m6(11) <= M6_degree(15 DOWNTO 8);
                    state := S00; 
                when S00 => 
                   crc_int <= x"0000";
                   crc_data <= m1(count1);
                   state := S0;
                    
                when S0 =>
                   crc_int <= crc_ret;
                   count1 := count1 + 1; 
                   crc_data<= m1(count1);
                   state := S1;
                                      
                when S1 =>
                    if count1 < 11 then
                         state := S0;
                    else
                         state := S2;
                         count1 := 0;
                         TMP := crc_ret;
                    end if;    

                when S2 => 
                    
                    m1(12) <= crc_ret(7 downto 0);
                    m1(13) <= crc_ret(15 downto 8);
                    crc_int <= x"0000";
                    crc_data <= m2(count1);                    
                    state := S3;
                      
                when S3 =>
                    crc_int <= crc_ret;
                    count1 := count1 + 1; 
                    crc_data<= m2(count1);
                    state := S4;
                        
                when S4 =>
                    if count1 < 11 then
                         state := S3;
                    else
                         state := S5;
                         count1 := 0;
                         TMP := crc_ret;
                    end if; 
                                       
                when S5 =>
                   
                    m2(12) <= crc_ret(7 downto 0);
                    m2(13) <= crc_ret(15 downto 8);                    
                    crc_int <= x"0000";
                    crc_data <= m3(count1);                    
                    state := S6; 
                when S6 =>
                    crc_int <= crc_ret;
                    count1 := count1 + 1; 
                    crc_data<= m3(count1);
                    state := S7;
                when S7 =>
                    if count1 < 11 then
                         state := S6;
                    else
                         state := S8;
                         count1 := 0;
                         TMP := crc_ret;
                    end if;

                when S8 =>
                    
                    m3(12) <= crc_ret(7 downto 0);
                    m3(13) <= crc_ret(15 downto 8);                    
                    crc_int <= x"0000";
                    crc_data <= m4(count1);                    
                    state := S9; 
                when S9 =>
                    crc_int <= crc_ret;
                    count1 := count1 + 1; 
                    crc_data<= m4(count1);
                    state := S10;
                when S10 =>
                    if count1 < 11 then
                         state := S9;
                    else
                         state := S11;
                         count1 := 0;
                         TMP := crc_ret;
                    end if;

                when S11 =>
                   
                    m4(12) <= crc_ret(7 downto 0);
                    m4(13) <= crc_ret(15 downto 8);                   
                    crc_int <= x"0000";
                    crc_data <= m5(count1);                    
                    state := S12; 
                when S12 =>
                    crc_int <= crc_ret;
                    count1 := count1 + 1; 
                    crc_data<= m5(count1);
                    state := S13;
                when S13 =>
                    if count1 < 11 then
                         state := S12;
                    else
                         state := S14;
                         count1 := 0;
                         TMP := crc_ret;
                    end if;

                when S14 =>
                    
                    m5(12) <= crc_ret(7 downto 0);
                    m5(13) <= crc_ret(15 downto 8);                    
                    crc_int <= x"0000";
                    crc_data <= m6(count1);                    
                    state := S15; 
                when S15 =>
                    crc_int <= crc_ret;
                    count1 := count1 + 1; 
                    crc_data<= m6(count1);
                    state := S16;
                when S16 =>
                    if count1 < 11 then
                         state := S15;
                    else
                         state := S17;
                         count1 := 0;
                         TMP := crc_ret;
                    end if;                                         

                when S17 =>  
                    m6(12) <= crc_ret(7 downto 0);
                    m6(13) <= crc_ret(15 downto 8);                    
                    m1a <= m1;
                    m2a <= m2;
                    m3a <= m3;
                    m4a <= m4;
                    m5a <= m5;
                    m6a <= m6;
                    state := S000;
                                       
                when others =>
                    state := S000;
            end case;
        end if;
    
    
    end process;
    process(CLK)
        variable state1 : StateType := S000;
        variable count2 : integer range 0 to 14;
    begin
        if RESET = '0' then
            state1 := S000;
            count2 := 0;
        elsif falling_edge(CLK) then  
             case state1 is
                when S000 => 
                    UartCtl <= '0';
                    UartData <= x"00";
                    state1 := S00;
                    count2 := 0;
 ---------------------------motor1--------------------------------                   
                when S00 =>
                    UartData <= m1a(count2);
                    state1 := S0;  
                                         
                when S0 =>
                    UartCtl <= '1';
                    count2 := count2 + 1;
                    state1 := S1; 
                                        
                when S1 =>
                    if UartBusy = '1' then
                        UartCtl <= '0';
                        state1 := S2;
                    end if;                        
                when S2 =>
                     if count2 < 14 then
                        state1 := S00;
                     else
                        state1 := S3;
                        count2 := 0;
                     end if; 

 ---------------------------motor2-------------------------------- 
                     
                 when S3 =>
                     UartData <= m2a(count2);
                     state1 := S4;  
                                          
                 when S4 =>
                     UartCtl <= '1';
                     count2 := count2 + 1;
                     state1 := S5; 
                                         
                 when S5 =>
                     if UartBusy = '1' then
                         UartCtl <= '0';
                         state1 := S6;
                     end if;                        
                 when S6 =>
                      if count2 < 14 then
                         state1 := S3;
                      else
                         state1 := S7;
                         count2 := 0;
                      end if;                      

 ---------------------------motor3-------------------------------- 

                                            
                  when S7 =>
                      UartData <= m3a(count2);
                      state1 := S8;  
                                           
                  when S8 =>
                      UartCtl <= '1';
                      count2 := count2 + 1;
                      state1 := S9; 
                                          
                  when S9 =>
                      if UartBusy = '1' then
                          UartCtl <= '0';
                          state1 := S10;
                      end if;                        
                  when S10 =>
                       if count2 < 14 then
                          state1 := S7;
                       else
                          state1 := S11;
                          count2 := 0;
                       end if; 

 ---------------------------motor4-------------------------------- 

                when S11 =>
                    UartData <= m4a(count2);
                    state1 := S12;  
                                         
                when S12 =>
                    UartCtl <= '1';
                    count2 := count2 + 1;
                    state1 := S13; 
                                        
                when S13 =>
                    if UartBusy = '1' then
                        UartCtl <= '0';
                        state1 := S14;
                    end if;                        
                when S14 =>
                     if count2 < 14 then
                        state1 := S11;
                     else
                        state1 := S15;
                        count2 := 0;
                     end if; 
                     
 
 
 ---------------------------motor5--------------------------------  
                 when S15 =>
                     UartData <= m5a(count2);
                     state1 := S16;  
                                          
                 when S16 =>
                     UartCtl <= '1';
                     count2 := count2 + 1;
                     state1 := S17; 
                                         
                 when S17 =>
                     if UartBusy = '1' then
                         UartCtl <= '0';
                         state1 := S18;
                     end if;                        
                 when S18 =>
                      if count2 < 14 then
                         state1 := S15;
                      else
                         state1 := S19;
                         count2 := 0;
                      end if; 

 ---------------------------motor6-------------------------------- 

                 when S19 =>
                     UartData <= m6a(count2);
                     state1 := S20;  
                                          
                 when S20 =>
                     UartCtl <= '1';
                     count2 := count2 + 1;
                     state1 := S21; 
                                         
                 when S21 =>
                     if UartBusy = '1' then
                         UartCtl <= '0';
                         state1 := S22;
                     end if;                        
                 when S22 =>
                      if count2 < 14 then
                         state1 := S19;
                      else
                         state1 := S23;
                         count2 := 0;
                      end if; 
                      
                      
                                                                                        
                when S23 =>
                     state1 := S000;    
                when others =>
                     state1 := S000;  
              end case;              
        end if;
    end process;

end architecture;
