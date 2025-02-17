import tkinter as tk
from tkinter import messagebox

class rentalps:
    def __init__(self, root):
        self.root = root
        self.root.title("Rental PS Berkah")
        
        self.username = "admin" 
        self.password = "admin"
        
        self.halaman_login()
        
    def halaman_login(self):
        self.login_frame = tk.Frame(self.root, padx=10, pady=10)
        self.login_frame.pack(fill="both", expand=True)
        
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, pady=5, sticky="w")
        self.input_username = tk.Entry(self.login_frame, width=30)
        self.input_username.grid(row=0, column=1, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, pady=5, sticky="w")
        self.input_password = tk.Entry(self.login_frame, width=30, show="*")
        self.input_password.grid(row=1, column=1, pady=5)
        
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.validasi_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
    def validasi_login(self):
        username = self.input_username.get()
        password = self.input_password.get()
        
        if username == self.username and password == self.password:
            messagebox.showinfo("Login Berhasil", "Selamat datang!")
            self.login_frame.destroy()
            self.show_halaman_utama()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")
            
    def show_halaman_utama(self):
        self.rentals = []
        self.ps_prices = {"PS3": 3000, "PS4": 5000, "PS5": 10000}
        self.snack_prices = {
            "Mie Goreng": 7000,
            "Mie Rebus": 6000,
            "Es": 3000,
            "Rokok": 3000,
            "Seblak": 10000
        }
        
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill="both", expand=True)
        
        tk.Label(self.main_frame, text="Nama Penyewa:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(self.main_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.main_frame, text="ID PS:").grid(row=1, column=0, sticky="w", pady=5)
        self.ps_id_entry = tk.Entry(self.main_frame, width=30)
        self.ps_id_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.main_frame, text="Jam Sewa:").grid(row=2, column=0, sticky="w", pady=5)
        self.hours_entry = tk.Entry(self.main_frame, width=30)
        self.hours_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(self.main_frame, text="Game:").grid(row=3, column=0, sticky="w", pady=5)
        self.game_entry = tk.Entry(self.main_frame, width=30)
        self.game_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(self.main_frame, text="Makanan Tambahan (pisahkan dengan koma):").grid(row=4, column=0, sticky="w", pady=5)
        self.snack_entry = tk.Entry(self.main_frame, width=30)
        self.snack_entry.grid(row=4, column=1, padx=10, pady=5)
        
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.add_button = tk.Button(self.button_frame, text="Tambah Rental", command=self.add_rental)
        self.add_button.grid(row=0, column=0, padx=5)
        
        self.update_button = tk.Button(self.button_frame, text="Update Rental", command=self.update_rental)
        self.update_button.grid(row=0, column=1, padx=5)
        
        self.delete_button = tk.Button(self.button_frame, text="Hapus Rental", command=self.delete_rental)
        self.delete_button.grid(row=0, column=2, padx=5)
        
        self.view_button = tk.Button(self.button_frame, text="Lihat Semua Rental", command=self.view_rentals)
        self.view_button.grid(row=0, column=3, padx=5)
        
        self.price_list_button = tk.Button(self.button_frame, text="Lihat Daftar Harga", command=self.view_price_list)
        self.price_list_button.grid(row=0, column=4, padx=5)
        
        tk.Label(self.main_frame, text="Daftar Penyewaan dan Pembelian:").grid(row=6, column=0, sticky="w", pady=5)
        self.rental_listbox = tk.Listbox(self.main_frame, width=80, height=10)
        self.rental_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.rental_listbox.bind(self.on_select_rental)
        
        self.exit_button = tk.Button(self.button_frame, text="Keluar", command=self.keluar)
        self.exit_button.grid(row=0, column=5, padx=5)
    
    def keluar(self):
        self.main_frame.destroy()
        self.halaman_login()

    def on_select_rental(self):
        selection = self.rental_listbox.curselection()
        if selection:
            selected_rental = self.rentals[selection[0]]
            
            self.clear_entries()
            
            self.name_entry.insert(0, selected_rental['name'])
            self.ps_id_entry.insert(0, selected_rental['ps_id'])
            self.hours_entry.insert(0, str(selected_rental['hours'] - selected_rental['bonus_time']))  # Subtract bonus time to show original hours
            self.game_entry.insert(0, selected_rental['game'])
            self.snack_entry.insert(0, ', '.join(selected_rental['snacks']) if selected_rental['snacks'] else '')
            
    def refresh_rentals(self):
        self.rental_listbox.delete(0, tk.END)
        for rental in self.rentals:
            snack_summary = ", ".join(rental['snacks']) if rental['snacks'] else "Tidak ada makanan"
            rental_summary = (
                f"{rental['name']} - "
                f"PS: {rental['ps_id']} - "
                f"Jam: {rental['hours']} - "
                f"Game: {rental['game']} - "
                f"Makanan: {snack_summary} - "
                f"Total: Rp {rental['total_cost']:,}"
            )
            self.rental_listbox.insert(tk.END, rental_summary)
            
    def calculate_snack_cost(self, snack_list):
        total_cost = 0
        valid_snacks = []
        invalid_snacks = []
        
        for snack in snack_list:
            snack = snack.strip()
            if snack in self.snack_prices:
                total_cost += self.snack_prices[snack]
                valid_snacks.append(snack)
            elif snack:  
                invalid_snacks.append(snack)
                
        return total_cost, valid_snacks, invalid_snacks

    def add_rental(self):
        name = self.name_entry.get()
        ps_id = self.ps_id_entry.get().upper()
        game = self.game_entry.get()
        try:
            jam = int(self.hours_entry.get())
            if not name or not ps_id or not game or jam <= 0:
                raise ValueError("Semua field harus diisi dengan benar.")

            if ps_id not in self.ps_prices:
                raise ValueError("ID PS tidak valid. Pilih PS3, PS4, atau PS5.")

            snack_input = self.snack_entry.get()
            snack_list = [s.strip() for s in snack_input.split(",") if s.strip()]
            snack_cost, valid_snacks, invalid_snacks = self.calculate_snack_cost(snack_list)

            if invalid_snacks:
                messagebox.showwarning("Peringatan", f"Makanan tidak tersedia: {', '.join(invalid_snacks)}")

            harga_rental = self.ps_prices[ps_id] * jam
            total_harga = harga_rental + snack_cost
            
            bonus_waktu = 1 if total_harga > 20000 else 0

            rental = {
                "name": name,
                "ps_id": ps_id,
                "game": game,
                "hours": jam + bonus_waktu,
                "rental_cost": harga_rental,
                "snack_cost": snack_cost,
                "total_cost": total_harga,
                "bonus_time": bonus_waktu,
                "snacks": valid_snacks
            }
            self.rentals.append(rental)
            self.clear_entries()
            self.refresh_rentals()
            
            detail_message = f"Rental berhasil ditambahkan!\n\n"
            detail_message += f"Biaya Rental: Rp {harga_rental}\n"
            detail_message += f"Biaya Makanan: Rp {snack_cost}\n"
            detail_message += f"Total Biaya: Rp {total_harga}\n"
            detail_message += f"Bonus Waktu: {bonus_waktu} jam"
            
            messagebox.showinfo("Berhasil", detail_message)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_rental(self):
        selected_rental_index = self.rental_listbox.curselection()
        if selected_rental_index:
            name = self.name_entry.get()
            ps_id = self.ps_id_entry.get().upper()
            game = self.game_entry.get()
            try:
                hours = int(self.hours_entry.get())
                if not name or not ps_id or not game or hours <= 0:
                    raise ValueError("Semua field harus diisi dengan benar.")
                
                if ps_id not in self.ps_prices:
                    raise ValueError("ID PS tidak valid. Pilih PS3, PS4, atau PS5.")
                
                snack_input = self.snack_entry.get()
                snack_list = [s.strip() for s in snack_input.split(",") if s.strip()]
                snack_cost, valid_snacks, invalid_snacks = self.calculate_snack_cost(snack_list)

                if invalid_snacks:
                    messagebox.showwarning("Peringatan", f"Makanan tidak tersedia: {', '.join(invalid_snacks)}")

                rental_cost = self.ps_prices[ps_id] * hours
                total_cost = rental_cost + snack_cost
                bonus_time = 1 if total_cost > 20000 else 0
                
                updated_rental = {
                    "name": name,
                    "ps_id": ps_id,
                    "game": game,
                    "hours": hours + bonus_time,
                    "rental_cost": rental_cost,
                    "snack_cost": snack_cost,
                    "total_cost": total_cost,
                    "bonus_time": bonus_time,
                    "snacks": valid_snacks
                }
                self.rentals[selected_rental_index[0]] = updated_rental
                self.clear_entries()
                self.refresh_rentals()
                
                detail_pesanan = f"Rental berhasil diperbarui!\n\n"
                detail_pesanan += f"Biaya Rental: Rp {rental_cost}\n"
                detail_pesanan += f"Biaya Makanan: Rp {snack_cost}\n"
                detail_pesanan += f"Total Biaya: Rp {total_cost}\n"
                detail_pesanan += f"Bonus Waktu: {bonus_time} jam"
                
                messagebox.showinfo("Berhasil", detail_pesanan)
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Tidak ada rental yang dipilih untuk diperbarui!")
            
    def delete_rental(self):
        selected_rental_index = self.rental_listbox.curselection()
        if selected_rental_index:
            rental_to_delete = self.rentals[selected_rental_index[0]]
            confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus rental untuk '{rental_to_delete['name']}'?")
            if confirm:
                self.rentals.pop(selected_rental_index[0])
                self.refresh_rentals()
                messagebox.showinfo("Berhasil", "Rental berhasil dihapus!")
        else:
            messagebox.showerror("Error", "Tidak ada rental yang dipilih untuk dihapus!")
            
    def view_rentals(self):
        if not self.rentals:
            messagebox.showinfo("Info", "Tidak ada rental untuk diliat!")
        else:
            total_pendapatan = 0
            rental_details = []
            
            for i in self.rentals:
                total_pendapatan += i['total_cost']
                snack_list = ", ".join(i['snacks']) if i['snacks'] else "Tidak ada"
                rental_detail = (
                    f"Nama: {i['name']}\n"
                    f"PS: {i['ps_id']}\n"
                    f"Game: {i['game']}\n"
                    f"Jam: {i['hours']}\n"
                    f"Biaya Rental: Rp {i['rental_cost']}\n"
                    f"Makanan: {snack_list}\n"
                    f"Biaya Makanan: Rp {i['snack_cost']}\n"
                    f"Total: Rp {i['total_cost']}\n"
                    f"Bonus: {i['bonus_time']} jam\n"
                    f"{'='*30}"
                )
                rental_details.append(rental_detail)
            
            all_rentals = "\n".join(rental_details)
            summary = f"Daftar Rental Saat Ini:\n\n{all_rentals}\n\nTotal Pendapatan: Rp {total_pendapatan}"
            
            messagebox.showinfo("Semua Rental", summary)
            
    def view_price_list(self):
        ps_prices = "Harga Sewa PS:\n" + "\n".join(
            f"- {ps}: Rp {price:,}/jam" for ps, price in self.ps_prices.items()
            )
        
        snack_prices = "\nHarga Makanan Tambahan:\n" + "\n".join(
            f"- {snack}: Rp {price:,}" for snack, price in sorted(self.snack_prices.items())
        )
        
        additional_info = "\n\nBonus:\nDapatkan tambahan 1 jam gratis untuk total pembelian di atas Rp 20.000!"
        
        price_list_message = f"{ps_prices}\n{snack_prices}{additional_info}"
        
        messagebox.showinfo("Daftar Harga", price_list_message)
        
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.ps_id_entry.delete(0, tk.END)
        self.hours_entry.delete(0, tk.END)
        self.game_entry.delete(0, tk.END)
        self.snack_entry.delete(0, tk.END)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = rentalps(root)
    root.mainloop()
